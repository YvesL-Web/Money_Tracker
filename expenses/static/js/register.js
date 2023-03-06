const usernameField = document.querySelector('#usernameField');
const feedbackField = document.querySelector('.usernameFeedback');
// const usernameSuccessOutput = document.querySelector('.usernameSuccessOutput')

const emailField = document.querySelector('#emailField')
const emailFeedback = document.querySelector('.emailFeedback')

const showPasswordToggle = document.querySelector('.showPasswordToggle')
const passwordField = document.querySelector('#passwordField')

function handleToggleInput(e) {
    if (showPasswordToggle.textContent === "show password") {
        showPasswordToggle.textContent = "hide password"
        passwordField.setAttribute("type", "text")
    } else {
        showPasswordToggle.textContent = "show password"
        passwordField.setAttribute("type", "password")
    }
}

showPasswordToggle.addEventListener('click', handleToggleInput)


emailField.addEventListener('keyup', (e) => {
    const emailVal = e.target.value

    emailField.classList.remove('is-invalid')
    emailFeedback.style.display = "none"

    if (emailVal.length > 0) {
        fetch("/users/validate-email", {
            body: JSON.stringify({ email: emailVal }),
            method: 'POST',
        }).then(res => res.json()).then((data) => {
            if (data.email_error) {
                emailField.classList.add('is-invalid')
                emailFeedback.style.display = "block"
                emailFeedback.innerHTML = `<p>${data.email_error}</p>`
            }
        })
    }
})

usernameField.addEventListener('keyup', (e) => {
    const usernameVal = e.target.value
    usernameSuccessOutput.textContent = `Checking ${usernameVal}`

    usernameField.classList.remove('is-invalid')
    feedbackField.style.display = "none"

    if (usernameVal.length > 0) {

        fetch("/users/validate-username", {
            body: JSON.stringify({ username: usernameVal }),
            method: 'POST',
        }).then(res => res.json()).then((data) => {
            // usernameSuccessOutput.style.display = "none"
            if (data.username_error) {
                usernameField.classList.add('is-invalid')
                feedbackField.style.display = "block"
                feedbackField.innerHTML = `<p>${data.username_error}</p>`
            }
        })

    }
})