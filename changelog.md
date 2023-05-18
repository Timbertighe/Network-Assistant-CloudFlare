# CloudFlare Plugin Changelog
## Issue #1 (April-May 2023)
    Can't write two IP addresses to SQL (one is IPv6, the other is IPv4)
    Workaround is to strip out the IPv6 address before writing
    Also fixed a bug with timestamps, and extracting fields from webhooks
    Fixed, 19/05/2023
    

## 0.10
### Bug fixes
    Fixed a bug where timestamps couldn't be extracted


## 0.91
### Webhook Handling
    Better handling of fields in the webhook
    Restructured the class for better code flow
    Better handling of unknown or missing fields in the webhook
    
### SQL
    Added an SQL creation script
    Added SQL logging of events
    
### Bug Fixes
    Fixed a bug with timestamp handling


## 0.9
### General Improvements
    Improved message colouring in Teams
    Reformatted timestamps to be simpler, and in the local timezone
    Added handling for more webhook formats
    

## 0.8
### Initial Creation
    A new plugin
    Very simple for now; This will grow as we learn more about CloudFlare alerts
    
