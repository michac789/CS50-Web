document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');

  // Send mail when submit button in compose-view is pressed
  document.querySelector('#compose-form').onsubmit = send_email;
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

// TODO - Load appropriate mailbox
function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Make a GET request to /emails/<mailbox> to request email of particular mailbox
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
      console.log(emails);
      emails.forEach(email => {
        // Create new div with unique id for each email, showing the sender, subject and timestamp
        const sender = email.sender;
        const subject = email.subject;
        const timestamp = email.timestamp;

        // TODO - FIX UI
        var sender_html = document.createElement('h6');
        sender_html.append("Sender: ", sender);
        var subject_html = document.createElement('h5');
        subject_html.append("Subject: ", subject);
        var timestamp_html = document.createElement('h7');
        timestamp_html.append("Timestamp: ", timestamp);
        
        const emaildiv = document.createElement('div');
        emaildiv.append(sender_html, subject_html, timestamp_html);
        emaildiv.addEventListener('click', () => {
          open_email(email.id)
        });

        // Grey background for read emails, white background otherwise
        if (email.read === true){
          emaildiv.setAttribute("class", "read_div email_div");
        }
        else{
          emaildiv.setAttribute("class", "unread_div email_div");
        }
        
        // Append all the email div to the main html page
        document.getElementById("emails-view").append(emaildiv);
      })
  });
}

// TODO - Send mail
function send_email() {

  // Getting in values for recipients, subject and body
  const value_recipients = document.querySelector('#compose-recipients').value;
  const value_subject = document.querySelector('#compose-subject').value;
  const value_body = document.querySelector('#compose-body').value;

  // Make POST request to /emails to send email
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: value_recipients,
        subject: value_subject,
        body: value_body
    })
  })
  .then(response => response.json())
  .then(result => {
      console.log(result);
  })
  .catch(error => console.log(error));
  localStorage.clear();

  // Load the user's sent mailbox
  //TODO - DELAY WHEN LOADING THE SENT TAB
  load_mailbox('sent');
  return false;
}

function open_email(email_id) {
  console.log("clicked")
  console.log(email_id)
  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {
      // Print email
      console.log(email);
  
      // ... do something else with email ...

  });
}
