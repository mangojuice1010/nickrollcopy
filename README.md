# Nickroll
A rickrolling practice bot that times individual practice sessions very simplistically.

## Description

Nickroll is a Python library for counting practice time in the private HCLC Discord server. It can do the following: starts counting practice time, allows pausing and resuming of practice timer, stops counting time of current practice session, sends a customized hello when any user types hello, a surprise for hungrybois, and replies with a help menu featuring all possible commands when mentioned or replied to

## Usage

$help - returns practice and stop commands

$practice - returns acknowledgment of timer start

$pause - pauses timer during practice

$resume - resumes timer during practice

$time - counts total practice time of current session

$stop - returns timer end and total practice time of session (minus any pauses)

@Nickroll - returns description of possible commands

## Contributing
For major changes, please open an issue first to discuss what you would like to change.

Future changes to consider: Array of rng emoji reactions; Total practice time from each member stored in individual profiles, rather than just individual practice sessions; Check if user is in voice channel before starting timer (currently allows offline practice); Streamlining code with separately implemented Timer class; Sending error messages during exceptions (currently bot is designed to only respond to appropriate use of commands while simply ignoring illogical series of events (such as $pause when $practice has not been called, or $resume when $pause has not been called)

## Contributors

mintchoco

Please make sure to update tests as appropriate.

## License
HAHA NONE why would I license this
