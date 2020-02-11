from pyfiglet import Figlet
from colorama import init
from colorama import Fore, Back, Style
import click
import uuid
import boto3
import json
import time

init()

aws_client = boto3.client('stepfunctions')

__version__ = '0.1.2'

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
# TODO Log state transitions
# TODO Add support for local and S3 input
# TODO Add support for local and S3 log output
def run(arn, input):
  """Run State Machine"""
  execution_name = str(uuid.uuid4())
  print('State Machine ARN: ' + arn)
  print('Execution name: ' + execution_name)
  print('Input: ' + input)
  print('Starting execution ...')

  response = aws_client.start_execution(
    stateMachineArn = arn,
    name = execution_name,
    input = input
  )

  if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
    print('Execution started succesfully.')
    time.sleep(1)
    status = getStatus(response['executionArn'])
    if status == 'RUNNING':
      print('Running ...')
    while status == 'RUNNING':
      time.sleep(1)
      status = getStatus(response['executionArn'])
    if status == 'FAILED':
      print('Job failed.')
    elif status == 'TIMED_OUT':
      print('Job timed out.')
    elif status == 'ABORTED':
      print('Job aborted.')
    elif status == 'SUCCEEDED':
      print('Job succeeded.')

def getStatus(arn):
  response = aws_client.describe_execution(
    executionArn = arn
  )
  return response['status']