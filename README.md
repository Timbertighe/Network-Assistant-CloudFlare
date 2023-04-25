# CloudFlare plugin
Handles webhooks from the CloudFlare platform

# Using the plugin
## Webhooks
### Enabling Webhooks
    This requires webhook alerts to be configured on CloudFlare
    This uses a global webhook definition
    Then, enable the webhook as an alert destination on individual services
    
### Webhook Authentication
    CloudFlare webook authentication uses the 'cf-webhook-auth' header
    This contains a secret that is defined in the cloudflare platform
    This secret is sent in plain text
    

## Configuration
### Overview
    Plugin configuration is in the 'config.yaml' file
    
#### Plugin Config
    Set 'webhook_secret' to the secret, as set in the CloudFlare webhook configuration
    Set the 'auth_header' to cf-webhook-auth


&nbsp;<br>
- - - -
## Files
### config.yaml
    A YAML file that contains all the config for the plugin
    This includes:
        * webhook_secret - The secret we expect to see from the device sending the webhook
        * auth_header - The header we expect to see in the webhook message
        * chat_id - The chat ID to send alerts to

&nbsp;<br>
### cloudflare.py
    The CloudFlareHandler class that handles events as they are received
    
#### __init__()
        Constructs the class

        Loads the configuration file
        Sets the table to '', as there is no SQL yet

        Parameters
        ----------
        None

        Raises
        ------
        None

        Returns
        -------
        None
        
#### timestamp()
        Reformat the timestamp to make it nicer

        The timestamp field in the webhook can vary, depending on the alert
        Extracts the timestamp from the webhook
        Converts to a datetime object
        Converts to the local timezone (original is in UTC)
        Simplifies the time format

        Parameters
        ----------
        json : json data
            The webhook (or part of it) that contains the timestamp

        Raises
        ------
        None

        Returns
        -------
        timestamp : str
            The simplified timestamp
            
#### fields()
        Extract fields from the webhook

        Parameters
        ----------
        json : json data
            The webhook (or part of it) that contains the fields we need

        Raises
        ------
        None

        Returns
        -------
        fields : dict
            A dictionary of fields we can use
            
#### handle_event()
    Handles a webhook when it arrives
        'raw_response' is the raw webhook
        'src' is the IP that sent the webhook
    Creates a dictionary of useful information
    Creates a message for the user
    Sends the message to teams

#### authenticate()
        Authenticate a webhook

        Checks that the webhook has been sent from a reliable source
        Checks that the correct header exists in the webhook
        Compares the password to the one we have in our config
        CloudFlare sends the passwords in plain text

        Parameters
        ----------
        request : requests object
            The raw webhook, including headers
        plugin : list
            The list of plugin configuration

        Raises
        ------
        None

        Returns
        -------
        True : Boolean
            If the webhook is authenticated
        False : Boolean
            If authentication failed
