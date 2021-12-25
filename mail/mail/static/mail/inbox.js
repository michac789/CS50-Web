document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', () => compose_email("", "", ""));

  // By default, load the inbox
  load_mailbox('inbox');

  // Send mail when submit button in compose-view is pressed
  document.querySelector('#compose-form').onsubmit = send_email;
});

function compose_email(def_recipient, def_subject, def_body) {

  // Assign default values (needed for reply feature, otherwise empty); Clear composition field
  document.querySelector('#compose-recipients').value = def_recipient;
  document.querySelector('#compose-subject').value = def_subject;
  document.querySelector('#compose-body').value = def_body;

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#mail-view').style.display = 'none';
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
        // Create some divs for each email's component, which is the sender, subject and timestamp
        let sender_html = document.createElement('div');
        let subject_html = document.createElement('div');
        let timestamp_html = document.createElement('div');
        sender_html.append(email.sender);
        subject_html.append(email.subject);
        timestamp_html.append(email.timestamp);

        // One row div to display one single email, opening a particular mail when clicked
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

  if (value_recipients === ""){
    alert("Invalid recipient! Please retry again!");
    compose_email("", "", "");
    return false;
  }

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
  .then(result => {console.log(result);})
  .catch(error => console.log(error));
  localStorage.clear();

  // Load the user's sent mailbox, short delay to ensure newly sent emails are loaded
  setTimeout(() => {load_mailbox('sent');}, 500);
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

      // Show email's sender, recipients, subject, timestamp
      elements1 = ["Sender:", "Recipient:", "Subject:", "Timestamp:"];
      elements2 = [email.sender, email.recipients, email.subject, email.timestamp];
      const emaildiv = document.createElement('div');
      for (let i = 0; i < 4; i++){
        let new_div1 = document.createElement('div');
        let new_div2 = document.createElement('div');
        let row_div = document.createElement('div');
        let bold_text = document.createElement('strong');
        row_div.setAttribute("class", "email_open_div");
        bold_text.append(elements1[i]);
        new_div1.append(bold_text);
        new_div2.append(elements2[i]);
        row_div.append(new_div1, new_div2);
        emaildiv.append(row_div);
      }
      document.getElementById("mail-view").append(emaildiv);

      // Button to reply an email
      if (mailbox === "inbox"){
        const reply_button = document.createElement('button');
        reply_button.innerHTML = "Reply Email";
        reply_button.setAttribute("id", "reply");
        document.getElementById("mail-view").append(reply_button);

        var pre_recipient = email.sender;
        var pre_subject = email.subject;
        if (email.subject.substring(0, 4) != "Re: ")
        {
          pre_subject = `Re: ${email.subject}`;
        }
        var pre_body = `On ${email.timestamp} ${email.sender} wrote: "${email.body}"\n`;
        
        document.querySelector('#reply').onclick = () => {
          compose_email(pre_recipient, pre_subject, pre_body)
        }
      }

      // Button to archive or unarchive for inbox & archived category
      if (mailbox != "sent"){
        document.getElementById("mail-view").append("  ")
        const new_button = document.createElement('button');
        if (email.archived === true){
          new_button.innerHTML = "Unarchive";
        } else {
          new_button.innerHTML = "Archive";
        }
        new_button.setAttribute("id", "archive");
        document.getElementById("mail-view").append(new_button);

        // Archive or unarchive when button is pressed & reload mailbox
        document.querySelector('#archive').onclick = () => {
          archive(email.id, email.archived, mailbox)
        }
      }

      // Show email's body (content)
      let horizontal_line = document.createElement('hr');
      document.getElementById("mail-view").append(horizontal_line);
      let body_html = document.createElement('div');
      body_html.append(email.body);
      document.getElementById("mail-view").append(body_html);
  });

  // Mark the email is read using PUT request
  fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  })
}

function archive(email_id, archive_status, mailbox) {
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
  setTimeout(() => {open_email(email_id, mailbox);}, 400);
}

// Possible improvements:
// Notify the user that email is not sent if recipient is invalid
// Scrolling feature
// Animation when putting emails in archive
