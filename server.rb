require 'rubygems'
require 'sinatra'

get "/set/:block/:color" do
  block = params[:block]
  color = params[:color]
  output = `python p2pclient.py set #{block} #{color}`
  output
end

get "/get/:block" do
  block = params[:block]
  output = `python p2pclient.py get #{block}`
  output
end
