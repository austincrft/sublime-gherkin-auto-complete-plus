# Gherkin Auto-Complete Plus
[![Build Status](https://travis-ci.org/austincrft/sublime-gherkin-auto-complete-plus.svg?branch=master)](https://travis-ci.org/austincrft/sublime-gherkin-auto-complete-plus)

This is a [Sublime Text](http://www.sublimetext.com/) auto-complete package for use with [Cucumber](https://cucumber.io/)'s [Gherkin](https://cucumber.io/docs/reference#gherkin) language. This package will catalog Gherkin step definitions from the `*.feature` files of the selected directories and provide auto-complete suggestions based on the catalogued steps.

![example](/img/sublime_gherkin_auto_complete_plus.gif)

*(apparently math isn't my forte)* :wink:


## Usage Info
 **This package is only compatible with Sublime Text 3. It will not work on Sublime Text 2.**
* Step catalog is updated when the package loads or on the save of a `*.feature` file
* This package relies on the first word of the line being a keyword (`Given`, `When`, `Then`) in order to give auto-complete suggestions. If a keyword is not found on the current line, the previous one will be used.
* It is not recommended that this is used alongside [cucumber-sublime-bundle](https://github.com/drewda/cucumber-sublime-bundle), as the bundled auto-complete will interfere with the results. At the moment, I've included the Gherkin syntax files so that this package can be self-contained. I have tried contacting the owner of that bundle, but he is not an easy man to reach.


## Config/Setup
1. From the toolbar, select `Preferences -> Package Settings -> Gherkin Auto-Complete Plus -> Settings - User` (Note: You can open `Settings - Default` as a reference)
2. Format the `Settings - User` in the following format:

      ```javascript
      {
          // A collection of the directories containing the features files you would like to scan
          "feature_file_directories":
          [
            "path/to/feature/files/directory",
            "some/path/to/different/feature/files/directory"
          ],

          // Logging for execution information -- this will output to the Sublime Text Console
          // You can view the console by going to the toolbar and selecting `View -> Show Console`
          // Valid options:
          // DEBUG - Detailed information for debugging
          // INFO - Confirmation that things are working as expected
          // WARNING - An indication something might fail in the future
          // ERROR - An error occurred, likely a recoverable one
          // CRITICAL - A non-recoverable error -- execution will stop
          "logging_level": "error"
      }
      ```


## Why did you create a new Gherkin Auto-Complete package instead of contributing to the existing one?
Short answer: There were a lot of changes I wanted to make, and felt it warranted a new package.

Differences:
* The auto-complete suggestions will pop up as you type -- no need to open manually
* Pressing <kbd>space</kbd> does not automatically commit the highlighted suggestion, so it shouldn't interrupt your workflow
* Only gives suggestions for current step-type (if the line starts with `Given`, then only `Given` steps will be suggested)
* Steps are formatted in snippet-notation to allow tabbing to values
* Table rows are not catalogued, which are unlikely to be duplicated exactly
* Values in between quotes (single and double), less- and greater-than signs, and numbers in 'integer' and 'decimal' format are standardized to remove duplicates from the step list
* A list of directories are specified explicitly instead of scanning all the folders and files open in Sublime Text (can be an issue for large projects)


## Isn't the name 'Gherkin Auto-Complete *Plus*' a bit arrogant?
Absolutely, yes. It's intended to be tongue-in-cheek, but also I couldn't think of a better name. :smirk:


## Installation
#### Automatic - via [Package Control](https://packagecontrol.io/)
    Search for 'Gherkin Auto-Complete Plus'
#### Mac OSX
    cd ~/Library/Application\ Support/Sublime\ Text\ 3/Packages
    git clone git://https://github.com/austincrft/sublime-gherkin-auto-complete-plus.git "Gherkin Auto-Complete Plus"
#### Linux
    cd ~/.config/sublime-text-3/Installed\ Packages
    git clone git://https://github.com/austincrft/sublime-gherkin-auto-complete-plus.git "Gherkin Auto-Complete Plus"
#### Windows
    cd Users/<user>/AppData/Roaming/Sublime\ Text\ 3/Installed\ Packages/
    git clone git://https://github.com/austincrft/sublime-gherkin-auto-complete-plus.git "Gherkin Auto-Complete Plus"


## Credits
The accompanied `*.tmLanguage` files were taken from [@drewda](https://github.com/drewda)'s [cucumber-sublime-bundle](https://github.com/drewda/cucumber-sublime-bundle) repository.
