
use std::env;

use tsd::Tsd;

fn main() {
    let args: Vec<String> = env::args().collect();

    if args.len() < 3 {
        println!("tsd [m3u8-url] [output] [-p|--proxy]");
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

    let proxy: Option<String> = match args.get(3) {
        Some(proxy) => {
            if proxy.starts_with("-p") {
                args.get(4).map(|v| {
                    v.clone()
                })
            }
            else if proxy.starts_with("--proxy="){
                let p: Vec<&str> = proxy.split("--proxy=").collect();
                p.get(0).map(|v| {
                    String::from(*v)
                })
            }
            else {
                None
            }  
        },
        None => None
    };

    let tsd = match Tsd::new(m3u8_url.clone(), output.clone(), proxy) {
        Ok(tsd) => tsd,
        Err(e) => panic!("{:?}", e)
    };
    tsd.exec();
}
