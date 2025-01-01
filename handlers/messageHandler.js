// whatsapp/handlers/messageHandlers.js

const Chance = require('chance');
const fs = require('fs');
const path = require('path');
const commands = require('../commands/index.js')
const download = require('../utils/download.js')
const solicitud = require('../utils/request.js');
const { measureMemory } = require('vm');

let statusp = false; // Estado inicial deshabilitado
const maxImages = 4; // Límite de imágenes
let imageCountp = 0;  // Contador de imágenes
let imagenes_formulario = '';
let download_complet = [];

module.exports = async (client, message) => {

    if (message.type === 'chat') {
        if (!message.body.startsWith('/') || message.body.length <= 1) return;

        const args = message.body.slice(1).trim().split(/ +/)
        const commandName = args.shift().toLowerCase()
        const command = commands.get(commandName)

        // console.log(command)

        await command.execute(client, message, args)

        if (args[0] === 'start') {

            imageCountp = command.getImageCount()
            // console.log(imageCountp)

            statusp = command.getStatus()
            // console.log(statusp) 

        }

    }
 
    if (message.type === 'image') {
        if (!statusp) {
            message.reply('🚫 El procesamiento de imágenes está deshabilitado. Usa /f start para habilitarlo.');
            return;
        }        

        const suministro = await download.mediaDownimage(message)

        // console.log(prediccion.suministro)
        
        download_complet.push(suministro?.file)
        
        if (download_complet.length === 4){

            const data = {
                [suministro.usuario]: download_complet
            };

            const jsonData = JSON.stringify(data); // Serializar a JSON
            const byteData = new TextEncoder().encode(jsonData); // Convertir a bytes
            const prediccion = await solicitud.localendpoint('prediccion',byteData)
            imagenes_formulario = prediccion.suministro
            // console.log(prediccion.suministro)
            download_complet.splice(0, download_complet.length);

            // const prediccion = await solicitud.localendpoint('prediccion',suministro.usuario)
        };


        
        // solicitud.popmensaje(prediccion, message)

        imageCountp++;

        // Comprueba si se alcanzó el límite
        if (imageCountp >= maxImages) {
            message.reply('⛔ iniciando resolucion formulario');
            statusp = false;
            console.log('⛔ iniciando resolucion formulario')
            // console.log(imagenes_formulario)
            formulario = await solicitud.localendpoint('prediccion','')
        }
    }
};
