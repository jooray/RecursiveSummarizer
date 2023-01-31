#!/usr/local/bin/python3
import openai
import os
from time import time,sleep
import textwrap
import re
import sys


def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()


def save_file(content, filepath):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)


def gpt3_completion(prompt, engine='text-davinci-003', temp=0.2, top_p=1.0, tokens=2000, freq_pen=0, pres_pen=0.0, stop=['<<END>>']):
    max_retry = 5
    retry = 0
    while True:
        try:
            response = openai.Completion.create(
                engine=engine,
                prompt=prompt,
                temperature=temp,
                max_tokens=tokens,
                top_p=top_p,
                frequency_penalty=freq_pen,
                presence_penalty=pres_pen,
                stop=stop)
            text = response['choices'][0]['text'].strip()
            text = re.sub('\s+', ' ', text)
            filename = '%s_gpt3.txt' % time()
            with open('gpt3_logs/%s' % filename, 'w') as outfile:
                outfile.write('PROMPT:\n\n' + prompt + '\n\n==========\n\nRESPONSE:\n\n' + text)
            return text
        except Exception as oops:
            retry += 1
            if retry >= max_retry:
                return "GPT3 error: %s" % oops
            print('Error communicating with OpenAI:', oops)
            sleep(1)

def create_summarization_prompt(text, context=None):
    prompt=list()
    if context is not None:
        prompt.append("This is a context for the next task:")
        prompt.append("")
        prompt.append("\""+context+"\"")

    prompt.append("The following is a section of the transcript of a video that should be summarized:")
    prompt.append("")

    prompt.append("\""+text+"\"")
    prompt.append("")

    prompt.append("Summarize this section of the transcript in a form of an English blog as if the speaker wrote it:")

    return '\n'.join(prompt)

def create_grand_summarization(text):
    prompt=list()
    prompt.append("These are summaries of a longer text:")
    prompt.append("")

    prompt.append("\""+text+"\"")
    prompt.append("")

    prompt.append("Summarize them in a form of an English blog as if the speaker wrote it:")

    return '\n'.join(prompt)


if __name__ == '__main__':
    alltext = open_file(sys.argv[1])
    chunks = textwrap.wrap(alltext, 3000)
    result = list()
    count = 0
    summary = None
    for chunk in chunks:
        count = count + 1
        prompt = create_summarization_prompt(chunk)
        prompt = prompt.encode(encoding='utf-8',errors='ignore').decode()
        summary = gpt3_completion(prompt)
        print('\n\n\n', count, 'of', len(chunks), ' - ', summary)
        result.append(summary)

    grand_summary=gpt3_completion(create_grand_summarization('\n'.join(result)))
    result.append('## Grand summary')
    result.append(grand_summary)

    save_file('\n\n'.join(result), sys.argv[2])