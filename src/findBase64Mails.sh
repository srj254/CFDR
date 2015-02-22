#!/bin/sh

grep -l -Z "Content-Transfer-Encoding: base64" * | xargs -0 -I'{}' mv '{}'  base64/
