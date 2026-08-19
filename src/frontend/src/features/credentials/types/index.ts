interface Signin {
    email: string,
    password: string
}

interface Signup extends Signin {
    password_2: string
}

interface Credentials extends Signin {
    password_2?: string
}

export type {
    Credentials,
    Signin,
    Signup
}