const qrcode = require('qrcode-terminal');
const fs = require("fs");
const { Client, LocalAuth } = require('whatsapp-web.js');
const client = new Client({
     authStrategy: new LocalAuth({
          clientId: "client-one"
     })
});

client.on('authenticated', (session) => {
    console.log(session);
});

client.initialize();
client.on("qr", qr => {
    qrcode.generate(qr, {small: true} );
});

function saveToFile(fileName, data) {
  fs.writeFile(fileName, data, function(err) {
    if (err) {
      console.error(err);
    } else {
      console.log(`Data berhasil disimpan ke dalam file  ${fileName}`);
    }
  });
}

client.on('ready', async () => {
  // Get the command line arguments
  const args = process.argv.slice(2);
  
  // Get the file name from the arguments
  const fileNameIndex = args.indexOf('-f');
  const fileName = fileNameIndex !== -1 ? args[fileNameIndex + 1] : 'number.txt';
  
  // Read the file
  fs.readFile(fileName, 'utf8', async (err, data) => {
    if (err) {
      console.error(err);
      return;
    }
    
    // Split the phone numbers into an array
    const lines = data.split('\n');
    for (let i = 0; i < lines.length; i++) {
      const phoneNumber = lines[i].trim();
      const isRegistered = await client.isRegisteredUser(phoneNumber);
      if (isRegistered) {
        console.log(`${phoneNumber} terdaftar di WhatsApp`);
        fs.appendFile('result\\valid.txt',phoneNumber + "\n", function (err) {
          console.log('Saved!');
      });
      } else {
        console.log(`${phoneNumber} tidak terdaftar di WhatsApp`);
        fs.appendFile('result\\invalid.txt',phoneNumber + "\n", function (err) {
          console.log('Saved!');
      });
      }
    }
  });
});
