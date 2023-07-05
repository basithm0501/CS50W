document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // 1. Send Mail
  document.querySelector('#compose-form').onsubmit = send_mail;

  // By default, load the inbox
  load_mailbox('inbox');
});

// 1. Send Mail
function send_mail() {
  const inpRecipients = document.querySelector('#compose-recipients').value;
    const inpSubject = document.querySelector('#compose-subject').value;
    const inpBody = document.querySelector('#compose-body').value;
    
    fetch('/emails', {
      method: "POST",
      body: JSON.stringify({
        recipients: inpRecipients,
        subject: inpSubject,
        body: inpBody,
        read: false
      })
    })
    .then(response => response.json())
    .then(result => {
      console.log(result)
    })

    load_mailbox('inbox')
}

// 3. View Email
function load_email(email) {

  // Clears the previously loaded emails
  document.querySelector('#single-view').innerHTML = ""

  // Show single view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#single-view').style.display = 'block';

  // Displays an email
  const top = document.createElement("div");
  top.innerHTML = `
  <strong>From: </strong>${email.sender}
  <br>
  <strong>To: </strong>${email.recipients}
  <br>
  <strong>Subject: </strong>${email.subject}
  <br>
  <strong>Timestamp: </strong>${email.timestamp}
  <hr>`;
  document.querySelector('#single-view').append(top);
  
  const body = document.createElement("p");
  body.innerHTML = email.body.replaceAll("\n", "<br>");
  document.querySelector('#single-view').append(body);

  fetch(`/emails/${email.id}`, {
    method: "PUT",
    body: JSON.stringify({
      read: true
    })
  })

  // 4. Archive and Unarchive

  // Ensures we are not in the sent tab.
  if (document.querySelector("#current-email").innerHTML != (`${email.sender}`)) {
    fetch(`/emails/${email.id}`)
    .then(response => response.json())
    .then(email => {
      const archive = document.createElement("button");
      archive.className = "btn btn-sm btn-outline-primary";
      archive.id = "archive-button";
      archive.style.margin = "5px";
      if (email["archived"] == true) {
        archive.innerHTML = "Unarchive"
      } else {
        archive.innerHTML = "Archive"
      }
      archive.onclick = () => archive_email(email);
      document.querySelector('#single-view').append(archive);

      if (email["read"] == true) {
        const read = document.createElement("button");
        read.className = "btn btn-sm btn-outline-primary";
        read.id = "read-button";
        read.innerHTML = "Mark as Unread";
        read.style.margin = "5px";
        read.onclick = () => mark_as_unread(email);
        document.querySelector('#single-view').append(read);
      }    
    })
  }

  // 5. Reply
  const reply = document.createElement("button");
  reply.className = "btn btn-sm btn-outline-primary"
  reply.id = "reply-button"
  reply.innerHTML = "Reply"
  reply.style.margin = "5px";
  reply.onclick = () => reply_email(email);
  document.querySelector('#single-view').append(reply);

}

function archive_email(email) {
  const newvalue = !email["archived"]
  fetch(`/emails/${email.id}`, {
    method: "PUT",
    body: JSON.stringify({
      archived: newvalue
    })
  })
  .then(update_load_mailbox("inbox"))
}

function mark_as_unread(email) {
  fetch(`/emails/${email.id}`, {
    method: "PUT",
    body: JSON.stringify({
      read: false
    })
  })
  .then(update_load_mailbox("inbox"))
}

function update_load_mailbox(mailbox) {
  load_mailbox(mailbox);
  location.reload();
}

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#single-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

// 5. Reply
function reply_email(email) {
  
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#single-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = `${email.sender}`;
  if (email.subject.startsWith("Re: ") == true) {
    document.querySelector('#compose-subject').value = `${email.subject}`;
  } else { 
    document.querySelector('#compose-subject').value = `Re: ${email.subject}`;
  }
  document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote: \n${email.body}\n\nReply: `;
}

function load_mailbox(mailbox) {
  
  document.querySelector('#emails-view').innerHTML = "";

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#single-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // 2. Mailbox
  fetch(`emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    console.log(emails);
    emails.forEach(email => {

      const emaildiv = document.createElement("div");
      const leftinfo = document.createElement("p");
      const rightinfo = document.createElement("p");

      leftinfo.innerHTML = `<strong>${email.sender}</strong>  ${email.subject}`;
      leftinfo.style.float = "left";
      leftinfo.style.color = "black";
      emaildiv.append(leftinfo);

      rightinfo.innerHTML = `${email.timestamp}`;
      rightinfo.style.float = "right";
      rightinfo.style.color = "#b5b5b5";
      emaildiv.append(rightinfo);

      emaildiv.style.border = "1px solid black";
      emaildiv.style.margin = "5px";
      emaildiv.style.padding = "5px";
      emaildiv.style.clear = "both";
      emaildiv.style.height = "36px";

      if (email.read === true) {
        emaildiv.style.background = "#f2f2f2";
      }

      const clickable = document.createElement("a");
      clickable.className = "emails";
      clickable.onclick = () => load_email(email);

      clickable.append(emaildiv);
      document.querySelector('#emails-view').append(clickable);

    })
  });
}