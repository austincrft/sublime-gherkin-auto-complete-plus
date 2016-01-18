# Gherkin Auto-Complete Plus
[![Build Status](https://travis-ci.org/austincrft/sublime-gherkin-auto-complete-plus.svg?branch=master)](https://travis-ci.org/austincrft/sublime-gherkin-auto-complete-plus)

This is a [Sublime Text](http://www.sublimetext.com/) auto-complete plugin for use with [Cucumber](https://cucumber.io/)'s [Gherkin](https://cucumber.io/docs/reference#gherkin) language. This plugin will catalog Gherkin step definitions from the `*.feature` files of the selected directories and provide auto-complete suggestions based on the catalogued steps.

![example](/img/sublime_gherkin_auto_complete_plus.gif)

*(apparently math isn't my forte)* :wink:

## Why did you create a new Gherkin Auto-Complete plugin instead of contributing to the existing one?
Short answer: There were a lot of changes I wanted to make, and felt it warranted a new plugin.

Differences:
* This plugin doesn't auto-commit the highlighted auto-complete entry on <kbd>space</kbd>, so it won't interrupt your workflow as much
* Only gives suggestions for current step-type (if the line starts with 'Given', then only 'Given' steps will be suggested)
* Steps are formatted in snippet-notation to allow tabbing to values
* Table rows are not catalogued, which are unlikely to be duplicated exactly
* Values in between quotes (single and double), less- and greater-than signs, and numbers in 'integer' and 'decimal' format are standardized to remove duplicates from the step list
* A list of directories are specified explicitly instead of scanning all the folders and files open in Sublime Text (can be an issue for large projects)


## Isn't the name 'Gherkin Auto-Complete *Plus*' a bit arrogant?
Absolutely, yes. It's intended to be tongue-in-cheek, but also I couldn't think of a better name. :smirk:

## Usage Info
* Step catalog is updated when the plugin loads, or a file is saved while in the Gherkin syntax
* Relies on the first word of the line being a keyword (`Given`, `When`, `Then`) in order to give auto-complete suggestions
* If the line begins with `And` or `But`, the previous keyword will be used
* It is not recommended that this is used alongside [cucumber-sublime-bundle](https://github.com/drewda/cucumber-sublime-bundle), as the bundled auto-complete will interfere with the results. At the moment, I've included the Gherkin syntax file so that this plugin can be self-contained, but I'll be contacting the owner of that bundle to see what we can work out.
* **This package is only compatible with Sublime Text 3. It will not work on Sublime Text 2.**


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
          ]
      }
      ```


## Credits
The accompanied `*.tmLanguage` files were taken from [@drewda](https://github.com/drewda)'s [cucumber-sublime-bundle](https://github.com/drewda/cucumber-sublime-bundle) repository.
