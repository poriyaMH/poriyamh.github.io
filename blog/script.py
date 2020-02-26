#!/usr/bin/python3
# Script to do the following:
# 1. pickup the markdown files in the markdown directory
# 2. generate the html output in a template and save in blog
# 3. update the links in index.html
# 4. remove the processed markdown file
import sys
import os
import fileinput

MARKDOWN_DIR = './markdown'
HTML_DIR = './post'
TEMPLATES_DIR = './templates'
INDEX = './index.html'

post_list = os.listdir(HTML_DIR)

title = 'test' # TODO:fix

try:
    import markdown
except ModuleNotFoundError:
    print("Error: this extension requires python3-markdown module.")
    sys.exit()

def update_post_list():
    global post_list
    post_list = os.listdir(HTML_DIR)

def make_index():
    update_post_list()
    posts_html_links = ''

    for filename in post_list:
        posts_html_links += f'<li><a href="post/{filename}">{filename}</a></li>'

    # Copy the template
    with open(INDEX, 'w') as index:
        with open(TEMPLATES_DIR + '/index.html', 'r') as template:
            for line in template.readlines():
               index.write(line) 
 
    with open(INDEX, 'r') as index_file:
        index_text = index_file.read()

    index_text = index_text.replace('{{links}}', posts_html_links)

    with open(INDEX, 'w') as index_file:
        index_file.write(index_text)

    print("Updated index.html.")

def generate_post(filename):
    """
    Generates html file based on the markdown provided as filename
    located in the MARKDOWN_DIR. Undefined behaviour if supplied with a
    filename that doesn't exist. If the post is already generated it will
    re-generate.
    """
    with open(MARKDOWN_DIR + '/' + filename + '.md') as input_file:
        md = input_file.read()

    html = markdown.markdown(md)

    # Copy the template
    with open(HTML_DIR + '/' + filename + ".html", 'w') as newfile:
        with open(TEMPLATES_DIR + '/post.html', 'r') as template:
            for line in template.readlines():
               newfile.write(line) 
    
    # Replace the variables
    with open(HTML_DIR + '/' + filename + ".html") as output:
        text = output.read()
    text = text.replace('{{title}}', title)
    text = text.replace('{{content}}', html)

    # Write the text back
    with open(HTML_DIR + '/' + filename + ".html", 'w') as output:
        output.write(text)

    print("generated " + filename + ".html")
    make_index()

def update_file(filename):
    if not filename.endswith('.md'):
        print(filename + " does not end with .md! skipping...")
    elif not os.path.isfile(MARKDOWN_DIR + '/' + filename):
        print(filename + " does not exist within the markdown directory.")
    else:
        filename = filename[:-3] # remove the .md at the end of the name
        generate_post(filename)

def remove_file(filename):
    if not filename.endswith('.md'):
        print(filename + " does not end with .md! skipping...")
    else:
        sure = input("Are you sure you want to delete the post" + filename +
        "? (y, N) ")
        if sure == 'y' or sure == 'Y':
            os.remove(MARKDOWN_DIR + '/' + filename)
            os.remove(HTML_DIR + '/' + filename[:-3] + '.html')
        make_index()

def regenerate():
    # check for MARKDOWN_DIR and iterate while it's not empty
    for filename in os.listdir(MARKDOWN_DIR):
        if not filename.endswith('.md'):
            print(filename + " does not end with .md! skipping...")
            continue
        else:
            filename = filename[:-3] # remove the .md at the end of the name
        generate_post(filename)


def main():
    # check for MARKDOWN_DIR and iterate while it's not empty
    for filename in os.listdir(MARKDOWN_DIR):
        if not filename.endswith('.md'):
            print(filename + " does not end with .md! skipping...")
            continue
        else:
            filename = filename[:-3] # remove the .md at the end of the name
        update_post_list()
        if filename + '.html' in post_list:
            continue
        generate_post(filename)


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        main()
    elif sys.argv[1] == 'edit':
        for item in sys.argv[2:]:
            update_file(item)
    elif sys.argv[1] == 'rm':
        for item in sys.argv[2:]:
            remove_file(item)
    elif sys.argv[1] == 'regenerate':
        regenerate()
