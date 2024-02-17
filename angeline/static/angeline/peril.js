// Adiciona um ouvinte de evento ao formulário para submissão
document.getElementById('form-completar').addEventListener('submit', function (event) {
    event.preventDefault(); // previne a submissão do formulário

    // Envia uma requisição assíncrona para o servidor
    fetch(event.target.action, {
        method: event.target.method,
        body: new FormData(event.target)
    })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('Erro ao completar perfil');
            }
        })
        .then(data => {
            // Esconde o formulário e mostra a mensagem de sucesso
            document.getElementById('form-completar').style.display = 'none';
            document.getElementById('success-message').style.display = 'block';
        })
        .catch(error => {
            console.error(error);
        });
});
