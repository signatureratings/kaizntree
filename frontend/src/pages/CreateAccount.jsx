import { useState } from "react"
import { Link, useNavigate, useNavigation } from "react-router-dom"

export function CreateAccount() {
  const [email, setEmail] = useState("")
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  const navigate = useNavigate()
  const navigation = useNavigation()
  const isSubmitting = navigation.state === "submitting"
  const register = async () => {
    try {
      //   const res = await fetch("/api/v1/auth/login")
      navigate("/login")
    } catch (error) {
      console.log(error)
    }
  }
  return (
    <div className="flex justify-center mt-20 ">
      <div className="w-80 h-80 flex flex-col rounded-md">
        <div className="flex items-center">
          <div>
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke-width="1.5"
              stroke="currentColor"
              class="w-8 h-8"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="m2.25 12 8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25"
              />
            </svg>
          </div>
          <div className=" font-bold text-4xl ml-5">Kaizntree</div>
        </div>
        <div className="mt-5">
          <input
            type="text"
            name="username"
            placeholder="username"
            className="rounded-md w-full border-2 pl-2 h-9"
            required="true"
            onChange={(e) => {
              setUsername(e.target.value)
            }}
            value={username}
          ></input>
        </div>
        <div className="mt-5">
          <input
            type="email"
            name="email"
            placeholder="email"
            className="rounded-md w-full border-2 pl-2 h-9"
            required="true"
            onChange={(e) => {
              setEmail(e.target.value)
            }}
            value={email}
          ></input>
        </div>
        <div className="mt-5">
          <input
            type="password"
            name="password"
            placeholder="password"
            className="rounded-md w-full border-2 pl-2 h-9"
            required="true"
            onChange={(e) => {
              setPassword(e.target.value)
            }}
            value={password}
          ></input>
        </div>
        <div className="flex justify-between mt-5">
          <button
            type="submit"
            className="rounded-md p-2 shadow-md bg-login tracking-widest"
            onClick={register}
            disabled={isSubmitting}
          >
            {isSubmitting ? "Submitting..." : "CREATE ACCOUNT"}
          </button>
          <Link
            className="rounded-md p-2 shadow-md bg-login font-sans tracking-widest"
            to="/login"
          >
            LOGIN
          </Link>
        </div>
        <div className="mt-2 text-blue-500">
          <Link className="underline">Forgot Password</Link>
        </div>
      </div>
    </div>
  )
}
