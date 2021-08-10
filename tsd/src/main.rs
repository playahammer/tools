
use std::env;

use tsd::Tsd;

fn main() {
    let args: Vec<String> = env::args().collect();

    if args.len() < 3 {
        println!("tsd [m3u8-url] [output]");
        return;
    }
    let m3u8_url =  match args.get(1) {
        Some(url) => url,
        None => panic!()
    };
    let output = match args.get(2) {
        Some(output) => output,
        None => panic!()
    };

    let tsd = match Tsd::new(m3u8_url.clone(), output.clone()) {
        Ok(tsd) => tsd,
        Err(e) => panic!("{:?}", e)
    };
    tsd.exec();
}
