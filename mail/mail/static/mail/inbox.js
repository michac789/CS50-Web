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
  document.querySelector('#mail-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#mail-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Make a GET request to /emails/<mailbox> to request email of particular mailbox
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
      console.log(emails);
      emails.forEach(email => {
        // Create new div with unique id for each email, showing the sender, subject and timestamp
        let sender_html = document.createElement('h6');
        sender_html.append("Sender: ", email.sender);
        let subject_html = document.createElement('h5');
        subject_html.append("Subject: ", email.subject);
        let timestamp_html = document.createElement('h7');
        timestamp_html.append("Timestamp: ", email.timestamp);

        // TODO - FIX UI
        
        // ??
        const emaildiv = document.createElement('div');
        emaildiv.append(sender_html, subject_html, timestamp_html);
        emaildiv.addEventListener('click', () => {
          open_email(email.id, mailbox)
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

function open_email(email_id, mailbox) {

  // Show mail view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#mail-view').style.display = 'block';
  document.getElementById("mail-view").innerHTML = "";

  // Make a GET request to /emails/<email_id>
  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {
      console.log(email);

      // Show email's sender, recipients, subject, timestamp, and body
      let sender_html = document.createElement('div');
      sender_html.append("Sender: ", email.sender);
      let recipients_html = document.createElement('div');
      recipients_html.append("Recipient: ", email.recipients);
      let subject_html = document.createElement('div');
      subject_html.append("Subject: ", email.subject);
      let timestamp_html = document.createElement('div');
      timestamp_html.append("Timestamp: ", email.timestamp);
      let body_html = document.createElement('div');
      body_html.append("Body: ", email.body);

      const emaildiv = document.createElement('div');
      emaildiv.append(sender_html, recipients_html, subject_html, timestamp_html, body_html);
      emaildiv.setAttribute("class", "mail_view");

      document.getElementById("mail-view").append(emaildiv);

      // Button to archive or unarchive for inbox & archived category
      if (mailbox != "sent"){
        const new_button = document.createElement('button');
        if (email.archived === true){
          new_button.innerHTML = "Unarchive";
        } else {
          new_button.innerHTML = "Archive";
        }
        new_button.setAttribute("id", "archive");
        document.getElementById("mail-view").append(new_button);
  
        // Archive or unarchive when button is pressed
        document.querySelector('#archive').onclick = () => {
          archive(email.id, email.archived)
        }
      }
  });

  // Mark the email is read using PUT request
  fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  })
}

function archive(email_id, archive_status) {
  // Archive or Unarchive email using PUT request
  value = true;
  if (archive_status){
    value = false;
  }
  console.log(value)
  fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
        archived: value
    })
  })
}
