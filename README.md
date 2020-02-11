# STail
CLI Tool to run and tail a step function synchronously.

Tail feature coming soon!

## Installation:
```bash
pip install stail
```

## Usage

### run
Runs a step function synchronously.
```bash
stail run --arn [state machine arn] --input [input]
```
####Options:
  --help  Show this message and exit.

##### Example:
```bash
stail run --arn arn:aws:states:<region>:955883056721:stateMachine:<name> --input "{\"param\":\"hello\"}"
```

### version
Displays the version.
```bash
stail version
```

Author: Iman Kamyabi
Feedback: contact@imankamyabi.com