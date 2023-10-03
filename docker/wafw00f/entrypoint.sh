#!/bin/sh

args=$@

# always log to stdout and as json -- so the subprocess can grab it.
wafw00f $@ --format=json --output=-

