const requests = require('../utils/request.js')

module.exports = {
    name: 'd',
    description: 'realiza la solictud a un endpoint sobre la actividad y retorna una respuesta',
    async execute(client, message, args) {
        const value = requests.localendpoint('actividad',args[0])
            .then(resultado =>{
                requests.popmensaje(resultado,message)
            })

            .catch(error =>{
                console.log(error);
            })
    }
};
