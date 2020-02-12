from pyfiglet import Figlet
from colorama import init
from colorama import Fore, Back, Style
from pathlib import Path
import click
import uuid
import boto3
import json
import time
import os
import json
import copy


init(autoreset=True)

aws_client = boto3.client('stepfunctions')

__version__ = '0.2.2'

@click.group()
def main():
  pass


@main.command()
def version():
  """Print Stail version"""
  f = Figlet(font='slant')
  print(f.renderText('Stail'))
  print("Version: " + Fore.GREEN + __version__)
  print(Style.RESET_ALL)

@main.command()
@click.option('--arn', prompt='State machine ARN', help='The ARN for the state machine.')
@click.option('--input', prompt='State machine input json', help='The input json for the state machine execution.')
def run(arn, input):
  """Run State Machine"""
  execution_name = str(uuid.uuid4())
  print('State Machine ARN: ' + Fore.CYAN + arn + Style.RESET_ALL)
  print('Execution name: ' + Fore.CYAN + execution_name + Style.RESET_ALL)
  print('Input: ' + Fore.CYAN + input + Style.RESET_ALL)

  print('Starting execution ...')

  response = aws_client.start_execution(
    stateMachineArn = arn,
    name = execution_name,
    input = input
  )

  if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
    print('Execution started succesfully.')
    print('Execution ARN: ' + Fore.CYAN + response['executionArn'] + Style.RESET_ALL)
    print('Execution Time: ' + Fore.CYAN + str(response['startDate']) + Style.RESET_ALL)
    time.sleep(1)
    status = getStatus(response['executionArn'])
    last_history_id = 0
    last_entered_time_seconds = 0
    Path('stail_logs').mkdir(parents=True, exist_ok=True)
    
    if status == 'RUNNING':
      print('')
    while status == 'RUNNING':
      time.sleep(1)
      exec_history_response = getExecutionHistory(response['executionArn'])
      for execution_event in exec_history_response['events']:
        if execution_event['id'] > last_history_id:
          last_history_id = execution_event['id']
          logged_object = copy.deepcopy(execution_event)
          logged_object['timestamp'] = str(logged_object['timestamp'])
          f = open('stail_logs/' + execution_name + '.log', 'a+')
          f.write(str(logged_object) + '\n')
          f.close()
          line = ''
          line = str(execution_event['id']).rjust(5, ' ') + ': '
          if 'stateEnteredEventDetails' in execution_event:
            print('')
          line = line +  execution_event['type'].ljust(30, ' ')
          line = line + ' ' + str(execution_event['timestamp'].strftime('%H:%M:%S.%f')[:-2])
          
          if execution_event['type'] == 'ExecutionStarted':
            line = line + Fore.GREEN + '     [START]' + Style.RESET_ALL
          if execution_event['type'] == 'TaskStateEntered':
            last_entered_time_seconds = execution_event['timestamp']
            line = line + Fore.GREEN + '     [' + execution_event['stateEnteredEventDetails']['name'] + ']' + Style.RESET_ALL
          if execution_event['type'] == 'TaskStateExited':
            task_duraction = execution_event['timestamp'] - last_entered_time_seconds
            line = line + Fore.GREEN + '     [' + execution_event['stateExitedEventDetails']['name'] + ']' + Style.RESET_ALL
            line = line + Fore.CYAN + '     (Duration: ' + str(task_duraction) + ' seconds)' + Style.RESET_ALL
          ERROR_STATES = ['ExecutionFailed', 'ActivityFailed', 'ActivityScheduleFailed', 'ActivityTimedOut', 'ExecutionAborted', 'ExecutionTimedOut', 'FailStateEntered', 'LambdaFunctionFailed', 'LambdaFunctionScheduleFailed', 'LambdaFunctionStartFailed', 'LambdaFunctionTimedOut', 'MapIterationAborted', 'MapIterationFailed', 'MapStateAborted', 'MapStateFailed', 'ParallelStateAborted', 'ParallelStateFailed', 'TaskFailed', 'TaskStartFailed', 'TaskStateAborted', 'TaskSubmitFailed', 'TaskTimedOut', 'WaitStateAborted']
          ERROR_DETAILS = ['activityScheduleFailedEventDetails', 'activityTimedOutEventDetails', 'taskFailedEventDetails', 'taskStartFailedEventDetails', 'taskSubmitFailedEventDetails', 'taskTimedOutEventDetails', 'executionFailedEventDetails', 'executionAbortedEventDetails', 'executionTimedOutEventDetails', 'lambdaFunctionFailedEventDetails', 'lambdaFunctionScheduleFailedEventDetails', 'lambdaFunctionStartFailedEventDetails', 'lambdaFunctionTimedOutEventDetails']
          if execution_event['type'] in ERROR_STATES:
            line = str(execution_event['id']).rjust(5, ' ') + ': '
            line = line +  Fore.RED + execution_event['type'].ljust(30, ' ') + Style.RESET_ALL
            line = line + ' ' + str(execution_event['timestamp'].strftime('%H:%M:%S.%f')[:-2])
          print(line)
          for error_type in ERROR_STATES:
            if execution_event['type'] == error_type:
              line = str(execution_event['id']).rjust(5, ' ') + ': '
              line = line +  Fore.RED + execution_event['type'].ljust(30, ' ') + Style.RESET_ALL
              line = line + ' ' + str(execution_event['timestamp'].strftime('%H:%M:%S.%f')[:-2])
              for error_detail_type in ERROR_DETAILS:
                if error_detail_type in execution_event:
                  print(Fore.RED + 'Error: ' +  Style.RESET_ALL + str(execution_event[error_detail_type]))
      status = getStatus(response['executionArn'])
    if status == 'FAILED':
      print(Fore.RED + 'Job failed.')
    elif status == 'TIMED_OUT':
      print(Fore.RED + 'Job timed out.')
    elif status == 'ABORTED':
      print(Fore.RED + 'Job aborted.')
    elif status == 'SUCCEEDED':
      print(Fore.GREEN +'Job succeeded.')
def getStatus(arn):
  response = aws_client.describe_execution(
    executionArn = arn
  )
  return response['status']

def getExecutionHistory(arn):
  response = aws_client.get_execution_history(
    executionArn = arn,
    maxResults = 1000,
  )
  return response
