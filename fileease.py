#!/usr/bin/env python3

import os
import shutil
import click

@click.command()
def main():
    logo_ascii = '''
    /$$$$$$$$ /$$ /$$           /$$$$$$$$
   | $$_____/|__/| $$          | $$_____/
   | $$       /$$| $$  /$$$$$$ | $$        /$$$$$$   /$$$$$$$  /$$$$$$
   | $$$$$   | $$| $$ /$$__  $$| $$$$$    |____  $$ /$$_____/ /$$__  $$
   | $$__/   | $$| $$| $$$$$$$$| $$__/     /$$$$$$$|  $$$$$$ | $$$$$$$$
   | $$      | $$| $$| $$_____/| $$       /$$__  $$ \____  $$| $$_____/
   | $$      | $$| $$|  $$$$$$$| $$$$$$$$|  $$$$$$$ /$$$$$$$/|  $$$$$$$
   |__/      |__/|__/ \_______/|________/ \_______/|_______/  \_______/
    '''

    colored_logo = click.style(logo_ascii, fg='green', bold=True)
    name = click.style('~ puang59 \n', fg='red', bold=True)
    click.echo(colored_logo)
    click.echo(name)

    try:
        def folder_prompt():
            while True:
                folder_path = click.prompt('What folder do you want to organize? (path) ')
                folder_path = os.path.expanduser(folder_path)  # Expand the ~ to the home directory
                if os.path.exists(folder_path) and os.path.isdir(folder_path):
                    files = os.listdir(folder_path)
                    return folder_path, files  # Return folder_path and files
                else:
                    print(f"The directory '{folder_path}' does not exist. Please try again.")

        try:
            folder_path, files = folder_prompt()
        except KeyboardInterrupt:
            print("\nOperation canceled")
            return
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return

        # Defining yes/no checks
        def get_yes_no_input(question):
            while True:
                response = click.prompt(question)
                if response.lower() in ("yes", "y"):
                    return True
                elif response.lower() in ("no", "n"):
                    return False
                else:
                    print("Invalid input. Please enter 'yes' or 'no'.")

        while True:
            organize_method = get_yes_no_input(f"Do you want keyword organizing? ({click.style('yes', fg='green')}/{click.style('no', fg='red')}) ")
            #For keyword mode 
            if organize_method:
                keyword = click.prompt("Enter Keyword ")
                master_folder_name = keyword
                total_files = 0
                for file in files:
                    if keyword.lower() in file.lower():
                        total_files += 1

                confirmation = get_yes_no_input(f"\n{click.style('Summary: ', fg='cyan')}\nMode -> Keyword organizing ({keyword})\nFolder -> {folder_path}\nMaster Folder -> {os.path.join(folder_path, keyword)}\nFiles -> {total_files-1} items\n\nContinue? ({click.style('yes', fg='green')}/{click.style('no', fg='red')}) ")
                if not confirmation:
                    print("Terminating!!")
                    return

                for file in files:
                    if keyword.lower() in file.lower():  # Check if keyword is present in the file name
                        source_path = os.path.join(folder_path, file)
                        target_directory = os.path.join(folder_path, master_folder_name)
                        if os.path.isdir(source_path):
                            continue
                        os.makedirs(target_directory, exist_ok=True)
                        shutil.move(source_path, os.path.join(target_directory, file))
                        click.echo(f"Moved {click.style(file, fg='magenta')} successfully")

                click.echo(f"{click.style('Done! Files are organized by keyword ;>', fg='green')}")
                return  # Exit without asking for extensions

            elif not organize_method:
                break
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")

        extensions_prompt = click.prompt('Extensions (example - jpg, png, gif) ')

        if "," in extensions_prompt:
            extensions_split = extensions_prompt.split(',')
        else:
            extensions_split = extensions_prompt.split(' ')

        extensions_list = [f".{ext.strip()}" for ext in extensions_split]

        diff_folder_prompt = get_yes_no_input(f"Do you want to create different folders for different extensions? ({click.style('yes', fg='green')}/{click.style('no', fg='red')}) ")
        master_folder_name = None

        if diff_folder_prompt:
            master_folder_prompt = get_yes_no_input(f"Do you want to create {click.style('Master Folder', fg='yellow')}? ({click.style('yes', fg='green')}/{click.style('no', fg='red')}) ")
            if master_folder_prompt:
                master_folder_name = click.prompt("What would be the name of your Master folder?")
                check_master = os.path.join(folder_path, master_folder_name)
                if os.path.exists(check_master):
                    overwrite_prompt = get_yes_no_input(
                        f"The folder '{master_folder_name}' already exists in the directory. Do you want to use it as your Master folder? " +
                        f"({click.style('yes', fg='green')}/{click.style('no', fg='red')}) ")
                    if not overwrite_prompt:
                        print("Terminating!!")
                        return
                else:
                    os.makedirs(check_master)
        else:
            master_folder_name = None

        total_files = 0
        for file in files:
            filename, extension = os.path.splitext(file)
            if extension.lower() in extensions_list:
                total_files += 1

        confirmation = get_yes_no_input(f"\n{click.style('Summary: ', fg='cyan')}\nMode -> Extension organizing \nFolder -> {folder_path}\nMaster Folder -> {os.path.join(folder_path, master_folder_name)} \nFiles -> {total_files} items\n\nContinue? ({click.style('yes', fg='green')}/{click.style('no', fg='red')}) ")
        if not confirmation:
            print("Terminating!!")
            return

        for file in files:
            filename, extension = os.path.splitext(file)
            if extension.lower() in extensions_list:
                target_directory = folder_path
                if diff_folder_prompt:
                    if master_folder_name:
                        target_directory = os.path.join(folder_path, master_folder_name, extension[1:])
                    else:
                        target_directory = os.path.join(folder_path, extension[1:])
                os.makedirs(target_directory, exist_ok=True)
                shutil.move(os.path.join(folder_path, file), os.path.join(target_directory, file))
                click.echo(f"Moved {click.style(file, fg='magenta')} successfully")

        click.echo(f"{click.style('Done! Files are organized ;>', fg='green')}")

    except (FileNotFoundError, PermissionError) as e:
        diff_folder_prompt = click.prompt(f"{click.style('Something went wrong!!!', fg='red')}\n\n")
        click.echo(f"Traceback:\n {e}")

if __name__ == '__main__':
    main()
