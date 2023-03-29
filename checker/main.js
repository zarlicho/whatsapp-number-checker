const qrcode = require('qrcode-terminal');
const fs = require("fs");
const cc = require("node-console-colors");
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
  const args = process.argv.slice(2);
  const fileNameIndex = args.indexOf('-f');
  const fileName = fileNameIndex !== -1 ? args[fileNameIndex + 1] : 'number.txt';
  fs.readFile(fileName, 'utf8', async (err, data) => {
    if (err) {
      console.error(err);
      return;
    }
    const lines = data.split('\n');
    for (let i = 0; i < lines.length; i++) {
      const phoneNumber = lines[i].trim();
      try{
        const isRegistered = await client.isRegisteredUser(phoneNumber);
        if (isRegistered) {
          console.log(cc.set("fg_green", `${phoneNumber} terdaftar di WhatsApp`))
          fs.appendFile('result\\valid.txt',phoneNumber + "\n", function (err) {
            console.log('Saved!');
        });
        } else {
          console.log(cc.set("fg_red", `${phoneNumber} tidak terdaftar di WhatsApp`))
          fs.appendFile('result\\invalid.txt',phoneNumber + "\n", function (err) {
            console.log('Saved!');
        });
        }
      } catch (error){
        console.log(cc.set("fg_yellow","error caused by phone number format!"))
      }
    }
    console.log("finish")
  });
});
