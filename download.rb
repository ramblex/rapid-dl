#!/usr/bin/ruby -wKU

# Download files directly from rapidshare given a URL such as:
# http://rapidshare.com/files/380428057/Avatar.2009.720p.BDRip.XviD.AC3-ViSiON.part02.rar
# See README for more information on setup and usage

require 'rubygems'
require 'choice'

@cookie = "rapidshare"

Choice.options do
  option :url do
    short '-u'
    long '--url=URL'
    desc 'The URL of the file to download'
  end
  
  option :file do
    short '-f'
    long '--file=FILE'
    desc 'File containing a list of URLs to download'
  end

  option :user do
    long '--user=USER'
    desc 'Your rapidshare username'
  end

  option :password do
    long '--password=PASSWORD'
    desc 'Your rapidshare password'
  end

  option :help do
    long '--help'
    desc 'Show this message'
  end
end

def download(url)
  # Find the actual URL
  %x[wget --load-cookies #{@cookie} -q #{url} -O test.tmp]
  server = %x[grep -m 1 action= test.tmp].split(/"/)[3]
  %x[wget --load-cookies #{@cookie} -q --post-data=dl.start=PREMIUM #{server} \
  -O test2.tmp]
  url = %x[grep /files test2.tmp | tail -1 ].split(/'/)[1]
  filename = %x[basename #{url}]
  puts "-> #{url}"
  %x[wget -b --load-cookies #{@cookie} #{url} -O #{filename}]
  File.delete "test.tmp"
  File.delete "test2.tmp"
end

if !File.file? @cookie 
  if Choice.choices[:user] and Choice.choices[:password]
    puts "Getting cookie..."
    %x[wget --no-check-certificate --save-cookies #{@cookie} \
  --post-data="login=#{Choice.choices[:user]}&password=#{Choice.choices[:password]}" \
  -O - https://ssl.rapidshare.com/cgi-bin/premiumzone.cgi > /dev/null]
    puts "SUCCESS: Put cookie into #{@cookie}"
  else
    puts "Please specify your rapidshare username and password. See help (-h)."
  end
end

if Choice.choices[:file] 
  if !File.file? Choice.choices[:file]
    puts "Could not find file '#{Choice.choices[:file]}'"
    exit
  end
  puts "Parsing file '#{Choice.choices[:file]}'..."
  for line in File.open(Choice.choices[:file]) do
    download(line.strip)
  end
elsif Choice.choices[:url]
  download(Choice.choices[:url])
else
  puts "Neither -f nor -u were specified...not downloading anything."
end
