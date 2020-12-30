# -*- coding: utf-8 -*-

from flask import render_template, send_file, redirect, url_for
from app import app
import os
import matplotlib.pyplot as plt
from app import driver

@app.route('/')
def index():
    
    return render_template('index.html')

@app.route('/result')
def jquery():
    
    hosts = driver.xml_reader('/home/pi/vulnerScan/website/app/static/files/result.xml')
    counter = 0
    
    for host in hosts:
    
        counter += 1
        filePath = f"/home/pi/vulnerScan/website/app/static/images/plot{counter}.png"
        title = host['address']
        
        chartPorts = []
        verifiedExploits = []
        possibleExploits = []
        
        if 'ports' in host:
            for port in host['ports']:
                
                chartPorts.append(port['port'])
                if 'active exploits:' in port:
                    verifiedExploits.append(port['active exploits:'])
                else:
                    verifiedExploits.append(0)
                    
                if 'exploits:' in port:
                    possibleExploits.append(port['exploits:'])
                else:
                    possibleExploits.append(0)
             
        # Generate plot
        
        fig, ax = plt.subplots()
        width = 0.35   
        ax.bar(chartPorts, verifiedExploits, width, label='Not confirmed exploits')
        ax.bar(chartPorts, possibleExploits, width, bottom=verifiedExploits,
               label='Exploits')
        
        ax.set_ylabel('Exploits')
        ax.set_title(title)
        
        ax.legend()

        plt.savefig(filePath)
        plt.clf()
    
    images = []
    
    for file in os.listdir('/home/pi/vulnerScan/website/app/static/images'):
        if file.endswith('.png'):
            images.append(os.path.join('/static/images', file))
        else:
            continue   
        
    return render_template('result.html', images=images)

@app.route('/upload')
def upload():
    
    return render_template('download.html')

@app.route('/download')
def download_file():
    
    path = '/home/pi/vulnerScan/website/app/static/files/result.xml'
    
    return send_file(path, as_attachment=True)

 
@app.route("/scan")
def resultView():
    
    return render_template("scan.html")

@app.route("/scanner")
def scanner():
    
    xmlFile = driver.nmap_scan()
    
    return redirect(url_for('jquery'))
    