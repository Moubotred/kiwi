const {MessageMedia } = require('whatsapp-web.js');
const axios = require('axios');
const path = require('path');

async function localendpoint(endpoint, suministro) {
    const url = `http://localhost:8000/${endpoint}`;
    const start = performance.now();
  
    try {
      const response = await axios.get(url, { params: { suministro: suministro } });
      const end = performance.now();
      const elapsed = (end - start) / 1000; // Ahora en segundos
      return {
        suministro: response.data.suministro,
        elapsed
      };
    } catch (error) {
      const end = performance.now();
      const elapsed = (end - start) / 1000; // Ahora en segundos
    //   let detail = "Error desconocido";
  
      if (error.response && error.response.data && error.response.data.detail) {
        detail = error.response.data.detail;
      } else if (error.response && error.response.data) {
        detail = JSON.stringify(error.response.data);
      }
  
      return { detail, elapsed };
    }
  }
  
function popmensaje(respuesta, message) {
    try {
    const suministro = respuesta.suministro;
    const elapsed = respuesta.elapsed;

    console.log(suministro)

    if (suministro.endsWith('.pdf')) {
        const pdfPath = `${__dirname}/descargas/pdf/${suministro}`;
        const pdf = MessageMedia.fromFilePath(pdfPath);
        message.reply(`✅ status: exito \n📌 mensaje: ${suministro}\n⏰ Tiempo: ${elapsed.toFixed(2)} s`, undefined, { media: pdf, quotedMessageId: message.id._serialized });
        console.log(`ReponsePython: envío exitoso ${suministro}`);

    } else if (suministro.endsWith('.png')) {
        const imagePath = `${__dirname}/descargas/png/${suministro}`;
        const image = MessageMedia.fromFilePath(imagePath);
        message.reply(`✅ status: exito \n📌 mensaje: ${suministro}\n⏰ Tiempo: ${elapsed.toFixed(2)} s`, undefined, { media: image, quotedMessageId: message.id._serialized });
        console.log(`ReponsePython: envío exitoso ${suministro}`);

    // } else if (suministro === "" ){
    //     console.log(`prediccion: \n${suministro}`)
        
    }


  
    } catch {
        const detail = respuesta.detail;
        const elapsed = respuesta.elapsed;
        message.reply(`❌ status: fallo \n${detail}\n⏰ Tiempo: ${elapsed.toFixed(2)} s`);
    }
  }

  module.exports = {
    localendpoint,
    popmensaje
};