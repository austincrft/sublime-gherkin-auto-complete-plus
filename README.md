GherkinAutocompletePlus
====================
GherkinAutocompletePlus is a [Sublime Text](http://www.sublimetext.com/) plugin that will catalog Gherkin step definitions from the `*.feature` files of the provided directory, and provide autocomplete suggestions based on the catalogued steps.

Why should I use this instead of [enter alternative plugin here]?
---
* It doesn't auto-commit selected Autocomplete entry on <kbd>space</kbd>, so it won't interrupt your workflow as much
* When cataloguing steps, it strips out values in between quotes (single and double), less- and greater-than signs, and numbers in 'integer' and 'decimal' format. This keeps duplicates out of the step list.
* When filling autocomplete list, it formats the steps in snippet notation


Example:


![scenarios](/images/scenario.png)


will create the following steps


![steps](/images/steps.png)


Installation
-------------
1. Open Sublime Text
2. From the toolbar, select `Preferences -> Browse Packages...`
3. Copy the folder `GherkinAutocompletePlus` to this directory
4. Restart Sublime Text
5. From the toolbar, select `Preferences -> Package Settings -> GherkinAutocompletePlus -> Settings - User` (Note: You can open `Settings - Default` as a reference)
6. Format the `Settings - User` in the following format:

      ```javascript
      {
          // The directory containing the features files you would like to scan
          "feature_file_directory": "path/to/featurefiles/directory",

          // The path to the file you would like to contain the steps
          "step_path": "path/to/steps.txt"
      }
      ```
      (Note: You will need to create the file `steps.txt`. **If you provide an existing file, the contents will be overriden.**)

7. Run the command to update steps from the toolbar: `Tools -> GherkinAutocompletePlus -> Update Steps`. If you'd like to verify that it worked, you can check the contents of the file you provided for `step_path` in the previous step above.
8. Create a new file and set the syntax to `Gherkin`. Type the first keyword (`Given`, `When`, `Then`) and first letter of the following intended word. **BAM!** It worked (hopefully).

Notes
------
* This plugin relies on the first word of the line being a keyword (`Given`, `When`, `Then`) in order to give autocomplete suggestions
* If you type one of the keywords `And` or `But`, it will check the first word of previous lines until it finds one or has no more lines to check
* The steps are not updated automatically. You will have to manually update the steps using the command under `Tools -> GherkinAutocompletePlus -> Update Steps` or use the hotkey (Default is `Ctrl+K, Ctrl+Z`).

TODO
-----
* Put on Sublime Text Package Manager
* Make OSX-friendly keybindings
* Automate updating steps, remove intermediate txt file
