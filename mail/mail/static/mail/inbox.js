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
  }

  // Query the API for the latest emails in that mailbox 

  // Display ???


// TODO - Send mail
function send_email() {

  alert(`sendddd`);

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
      // Print result
      console.log(result);
  })
  .catch(error => console.log(error));
  localStorage.clear();

  // Load the user's sent mailbox
  load_mailbox('sent');
  return false;
}
