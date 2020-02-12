# Stail
CLI Tool to run and tail a step function synchronously and persist event logs for the state machine execution on disk.

![Screenshot](https://raw.githubusercontent.com/imankamyabi/stail/master/images/console-screenshot.png)


## Installation:
```shell
pip install stail
```

## Usage

### run
Starts a step function execution synchronously, tails the event history to the console and create a log file with all the events for the execution.

Log file is stored at stail_logs/[execution name (UUID)].log 

```shell
stail run --arn [state machine arn] --input [input]
```
#### Options:
  --arn  State machine ARN
   
  --input Input JSON to the state machine

##### Example:
```shell
stail run --arn arn:aws:states:<region>:955883056721:stateMachine:<name> --input "{\"param\":\"hello\"}"
```

### version
Displays the version.
```shell
stail version
```

Author: Iman Kamyabi
 
Feedback: contact@imankamyabi.com