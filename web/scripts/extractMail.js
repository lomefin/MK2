var mailExists = function(email)
{
	for(var i = 0; i < invitees_emails.length ; i++)
	{
		if(invitees_emails[i] == email)
			return true;
	}
	return false;
}
var mailAlreadySent = function (email)
{
	for(var i = 0; i < invitees_invited.length ; i++)
	{
		if(invitees_invited[i] == email)
			return true;
	}
	return false;
}
var extractMails = function(el)
{
	var mailText = el.value;
	mailText = mailText.replace(';',',');
	el.value = mailText;
	
	possible_addresses = mailText.split(',');
	
	mailList = $('acceptedEmails');
	var filter = /^([a-zA-Z0-9_.-])+@(([a-zA-Z0-9-])+.)+([a-zA-Z0-9]{2,4})+$/;
	for ( var i=0;i < possible_addresses.length; i++ )
	{
		var possible_address = possible_addresses[i];
		
		if (filter.test(possible_address) && !mailAlreadySent(possible_address)) 
		{
			var li = new Element ('li');
			if(mailExists(possible_address) )
				li.style.color = "green";
			li.innerHTML = possible_address;
			li.injectInside(mailList);
		}
		
	}
	
	
	
}