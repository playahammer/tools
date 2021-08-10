extern crate m3u8_rs;
extern crate crypto;

use reqwest::Error;
use reqwest::blocking::Client;
use crypto::digest::Digest;
use crypto::sha1::Sha1;
use url::{ParseError, Url};

use std::io::{self, Write};
use std::fs::{self, File};
use std::process::Command;
use std::time::{SystemTime, SystemTimeError, UNIX_EPOCH};

pub struct Tsd{
      pub link: String,
      pub output: String,
      pub logs_file: String
}

#[derive(Debug)]
enum ErrorWrapper{
      IoError(io::Error),
      ReError(reqwest::Error)
}

impl From<io::Error> for ErrorWrapper{
      fn from(val: io::Error) -> Self {
            ErrorWrapper::IoError(val)
      }
}

impl From<reqwest::Error> for ErrorWrapper{
      fn from(val: reqwest::Error) -> Self {
            ErrorWrapper::ReError(val)
      }
}


fn sha1_gen(text: &str) -> String {
      let mut hasher = Sha1::new();
      hasher.input_str(text);
      hasher.result_str()
}

impl Tsd {
      pub fn new(link: String, output: String) -> Result<Tsd, SystemTimeError>{
            let start = SystemTime::now();
            let since_the_epoch = start.duration_since(UNIX_EPOCH)?;

            Ok(Tsd {
                  link,
                  output,
                  logs_file: format!("{}.log",since_the_epoch.as_micros())
            })
      }

      fn get_m3u8_source(&self) -> Result<String, Error> {
            let client = Client::new();
            let resp = client.get(&self.link).send()?;
            let text = resp.text()?;
            Ok(text)
      }

      fn parse_m3u8(&self, m3u8:String)-> Result<Vec<String>, String> {
            let bytes = m3u8.as_bytes();
            let mut playlist = Vec::new();

            let media_playlist = match m3u8_rs::parse_media_playlist_res(&bytes) {
                  Ok(pl) => pl,
                  Err(_) => return Err(String::from("Parsed m3u8 file error"))

            };

            for seg in media_playlist.segments.iter() {
                  playlist.push(seg.uri.clone());
            }
            Ok(playlist)

      }

      fn join_ts_link(&self, ts: Vec<String>) -> Result<Vec<String>, ParseError>{
            if ts.len() <= 0 {
                  return Ok(ts);
            }

            let mut ts_links = Vec::new(); 
            if &ts[0].starts_with("http") == &false{
                  for t in ts.iter() {
                        let base_url = Url::parse(&self.link)?;
                        let ts_link = base_url.join(t)?;
                        ts_links.push(String::from(ts_link.as_str()));
                  }
            }
            else { return Ok(ts) }
            Ok(ts_links)
      }

      fn download_ts(&self, ts_url: &String, saved_file_name: &str) -> Result<(), ErrorWrapper> {
            let client = Client::new();
            let mut bytes = client.get(ts_url).send()?;
            let mut output = File::create(format!("{}.ts", saved_file_name))?;
            io::copy(&mut bytes, &mut output)?;
            Ok(())
      }

      fn merge_media_files(&self, input_files: &Vec<String>, output_file: &String) -> Result<(), ErrorWrapper> {
            let mut logs = File::create(self.logs_file.clone())?;
            let input_file: Vec<String> = input_files.iter().map(|i| format!("file '{}.ts'", i)).collect();
            logs.write_all(input_file.join("\r\n").as_bytes())?;

            let mut ffmpeg = Command::new("ffmpeg");
            ffmpeg.args(["-f", "concat", "-i"])
                  .arg(self.logs_file.clone())
                  .args(["-c", "copy"])
                  .arg(output_file);
            ffmpeg.output()?;
            
            Ok(())
      }

      fn delete_slice_files(&self, files: Vec<String>) -> Result<(), ErrorWrapper>{
            for f in files.iter() {
                fs::remove_file(format!("{}.ts", f))?;
            }
            fs::remove_file(self.logs_file.clone())?;
            Ok(())
      }

      pub fn exec(&self){
            let m3u8 = match self.get_m3u8_source() {
                  Ok(text) => text,
                  Err(e) => panic!("{}", e)
            };
            let playlist = match self.parse_m3u8(m3u8) {
                  Ok(playlist) => playlist,
                  Err(e) => panic!("{}", e)
            };
            let playlist = match self.join_ts_link(playlist) {
                  Ok(playlist) => playlist,
                  Err(e) => panic!("{}", e)
            };

            println!("Ts slice file lists as follows:\n {:?}", playlist);

            let mut input_files = Vec::new();
            for pl in playlist.iter(){
                  loop {
                        print!("Downloading for {:?}...", pl);
                        let file_hash = sha1_gen(pl);
                        match self.download_ts(pl, &file_hash){
                              Ok(()) => {  input_files.push(file_hash); println!("Ok!"); break; },
                              Err(e) => { println!("Failed: {:?}", e)}
                        }
                  }
                
            }

            print!("Merging files...");
            match self.merge_media_files(&input_files, &self.output) {
                Ok(()) => println!("Ok!") ,
                Err(e) => println!("Failed: {:?}", e)
            }
            
            print!("Deleting files...");
            match self.delete_slice_files(input_files) {
                Ok(()) => println!("Ok!"),
                Err(e) => println!("Failed: {:?}", e) 
            }
            
      }     

}


