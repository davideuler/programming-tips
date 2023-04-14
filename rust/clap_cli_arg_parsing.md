# Command line argument parsing in Rust using Clap

For example, to create a project which could parse docx files into text.
We use docx-rs for file parsing.

Reference:
https://blog.logrocket.com/command-line-argument-parsing-rust-using-clap/


## setup project
Set up a project with cargo new arg-parser-demo in Rust. The src/main.rs file is now has the default main function:

```
cargo new arg-parser-demo
cd arg-parser-demo
```

```
fn main() {
    println!("Hello, world!");
}
```

Run the program

```
cargo run 
```

## add dependencies

```
  cargo add docx-rs
  cargo add clap
  cargo add serde_json
  cargo add anyhow
```

Will got these dependencies:
```
[dependencies]
docx-rs = "0.4.6"
clap = { version = "4.2.2", features = ["derive"] }
serde_json = "1.0.96"
anyhow = "1.0.70"
```

## add file content 
vim src/bin/docx_parser.rs

```
use clap::Parser;
use docx_rs::*;
use serde_json::Value;
use std::io::Read;

#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Args {
    #[arg(short, long)]
    name: String,
}

fn parse_docx(file_name: &str) -> anyhow::Result<()> {
    let data: Value = serde_json::from_str(&read_docx(&read_to_vec(file_name)?)?.json())?;
    if let Some(children) = data["document"]["children"].as_array() {
        children.iter().for_each(read_children);
    }
    Ok(())
}

fn read_children(node: &Value) {
    if let Some(children) = node["data"]["children"].as_array() {
        children.iter().for_each(|child| {
            if child["type"] != "text" {
                read_children(child);
            } else {
                println!("{}", child["data"]["text"]);
            }
        });
    }
}

fn read_to_vec(file_name: &str) -> anyhow::Result<Vec<u8>> {
    let mut buf = Vec::new();
    std::fs::File::open(file_name)?.read_to_end(&mut buf)?;
    Ok(buf)
}

fn main() -> anyhow::Result<()> {
    let args = Args::parse();
    parse_docx(&args.name)?;
    Ok(())
}
```

## Run the program to get input from command line argument
```
cargo run --bin docx_parser -- --name  ~/docs/demo.docx
```
