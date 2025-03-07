#!/usr/bin/env python3
"""
Script to deploy the generated website to a web server using FTP.
"""

import ftplib
import os
import argparse
from getpass import getpass

def upload_directory(ftp, local_dir, remote_dir):
    """Upload a directory and all its contents to the FTP server."""
    # Create remote directory if it doesn't exist
    try:
        ftp.mkd(remote_dir)
        print(f"Created directory: {remote_dir}")
    except:
        pass
    
    # Change to remote directory
    ftp.cwd(remote_dir)
    
    # Upload all files and subdirectories
    for item in os.listdir(local_dir):
        local_path = os.path.join(local_dir, item)
        
        if os.path.isfile(local_path):
            with open(local_path, 'rb') as file:
                ftp.storbinary(f'STOR {item}', file)
                print(f"Uploaded: {remote_dir}/{item}")
        elif os.path.isdir(local_path):
            upload_directory(ftp, local_path, item)
    
    # Go back to parent directory
    ftp.cwd('..')

def main():
    parser = argparse.ArgumentParser(description='Deploy website to FTP server')
    parser.add_argument('--host', required=True, help='FTP server hostname')
    parser.add_argument('--user', required=True, help='FTP username')
    parser.add_argument('--remote-dir', default='/', help='Remote directory to upload to')
    parser.add_argument('--local-dir', default='output', help='Local directory to upload from')
    
    args = parser.parse_args()
    
    # Get password securely
    password = getpass(f"Enter FTP password for {args.user}@{args.host}: ")
    
    try:
        # Connect to FTP server
        print(f"Connecting to {args.host}...")
        ftp = ftplib.FTP(args.host)
        ftp.login(args.user, password)
        print("Connected successfully!")
        
        # Upload files
        print(f"Uploading files from {args.local_dir} to {args.remote_dir}...")
        upload_directory(ftp, args.local_dir, args.remote_dir)
        
        # Close connection
        ftp.quit()
        print("Deployment complete!")
        
    except ftplib.all_errors as e:
        print(f"FTP error: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main() 