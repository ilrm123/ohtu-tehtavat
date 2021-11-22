*** Settings ***
Resource  resource.robot
Test Setup  Create User And Input Login Command

*** Test Cases ***
Register With Valid Username And Password
    Input Credentials  uusiu  salasana1
    Output Should Contain  New user registered

Register With Already Taken Username And Valid Password
    Input Credentials  kalle  validps
    Output Should Contain  User with username kalle already exists

Register With Too Short Username And Valid Password
    Input Credentials  u  validps
    Output Should Contain  ['Invalid username or password']

Register With Valid Username And Too Short Password
    Input Credentials  validus  p
    Output Should Contain  ['Invalid username or password']

Register With Valid Username And Long Enough Password Containing Only Letters
    Input Credentials  usernamee  passaword
    Output Should Contain  ['Invalid username or password']

*** Keywords ***
Create User And Input Login Command
    Create User  kalle  kalle123
    Input Login Command
