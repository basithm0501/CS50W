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

function send_mail() {
  const inpRecipients = document.querySelector('#compose-recipients').value;
    const inpSubject = document.querySelector('#compose-subject').value;
    const inpBody = document.querySelector('#compose-body').value;
    
    fetch('/emails', {
      method: "POST",
      body: JSON.stringify({
        recipients: inpRecipients,
        subject: inpSubject,
        body: inpBody
      })
    })
    .then(response => response.json())
    .then(result => {
      console.log(result)
    })

    load_mailbox('inbox')
}

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

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

      leftinfo.innerHTML = `<strong>${email.recipients}</strong>  ${email.subject}`;
      leftinfo.style.float = "left";
      emaildiv.append(leftinfo);

      rightinfo.innerHTML = `${email.timestamp} (${email.id}) <- TEMPORARY ID`;
      rightinfo.style.float = "right";
      rightinfo.style.color = "#b5b5b5";
      emaildiv.append(rightinfo);

      emaildiv.style.border = "1px solid black";
      emaildiv.style.margin = "5px";
      emaildiv.style.padding = "5px";
      emaildiv.style.clear = "both";
      emaildiv.style.height = "36px"

      if (email.read === true) {
        emaildiv.style.background = "#f2f2f2"
      }

      document.querySelector('#emails-view').append(emaildiv);

    })
  });

}