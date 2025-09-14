import React from 'react';
import { UserCircleIcon, LockClosedIcon } from '@heroicons/react/24/outline'; // For icons
import { useNavigate } from 'react-router-dom';
import { useState } from 'react';
import toast from 'react-hot-toast';


const LoginPage = () => {

    const [form, setForm] = useState({
        email: "",
        password: ""
    })
    const [loading, setLoading] = useState(false)
    const navigate = useNavigate();

    const handleChange = (e) => {
        setForm((prev) => ({
            ...prev,
            [e.target.id]: e.target.value,
        }));
    }

    const handleLogin = async (e) => {
        e.preventDefault();
        setLoading(true)

        try {
            const res = await fetch('http://localhost:8000/api/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(form),
                credentials: "include"
            })

            const data = await res.json()

            if (!data.error) {
                toast.success(`Login Success: ${data.message}`)
                window.location.href = `http://localhost:8501/?user_id=${form.email}`;
                console.log("Login Success")
            } else {
                toast.error("Login Failed : ", data.error)
                console.log("Login Failed")
            }
        } catch {
            toast.error("Login Failed")
            console.log("Login Failed")
        } finally {
            setLoading(false)
        }
    }


    return (
        <div className="min-h-screen flex items-center justify-center bg-dark-bg text-white relative overflow-hidden">
            {/* Abstract Wave Background (You might want to refine this with a more complex SVG or image) */}
            <div
                className="absolute top-0 right-0 w-3/5 h-full"
                style={{
                    background: 'linear-gradient(135deg, rgba(161,0,255,0.8) 0%, rgba(0,16,255,0.8) 50%, rgba(0,217,255,0.8) 100%)',
                    clipPath: 'polygon(25% 0%, 100% 0%, 100% 100%, 0% 100%)', // Creates a diagonal cut
                    // For a more wavy effect, you'd typically use a background SVG or a canvas animation
                    // For simplicity, we'll use a linear gradient with a clip-path for now to mimic the overall shape.
                }}
            >

            </div>

            {/* Login Form Card */}
            <form onSubmit={handleLogin}>
                <div className="relative z-10 p-10 py-5 rounded-xl shadow-2xl w-full max-w-md mx-4"
                    style={{ backgroundColor: 'rgba(28, 26, 47, 0.9)', backdropFilter: 'blur(10px)' }}>

                    <div className="flex justify-center mb-4">
                        <UserCircleIcon className="h-24 w-24 text-blue-400" />
                    </div>

                    <div className="form-control mb-4">

                        <label className="input-group input-group-md">
                            <span>
                                <UserCircleIcon className="h-7 w-7 text-gray-400 mb-1.5" />
                            </span>
                            <input
                                type="text"
                                id='email'
                                placeholder="Email"
                                value={form.email}
                                onChange={handleChange}
                                className="input input-bordered input-md w-full bg-gray-700 text-white border-gray-600 focus:border-blue-500 focus:ring-blue-500"
                            />
                        </label>
                    </div>

                    <div className="form-control mb-6">
                        <label className="input-group input-group-md">
                            <span>
                                <LockClosedIcon className="h-7 w-7 text-gray-400 mb-1.5" />
                            </span>
                            <input
                                type="password"
                                placeholder="password"
                                id='password'
                                name='password'
                                value={form.password}
                                onChange={handleChange}
                                className="input input-bordered input-md w-full bg-gray-700 text-white border-gray-600 focus:border-blue-500 focus:ring-blue-500"
                            />
                        </label>
                    </div>

                    <button
                        className="btn w-full text-white font-bold py-3 px-4 rounded-lg mb-4"
                        style={{ backgroundColor: '#ff007f', '&:hover': { backgroundColor: '#e60073' } }}
                        disabled={loading}
                    >
                        {loading ? (
                            <>
                                <span className="loading loading-spinner"></span>
                                Logging in...
                            </>
                        ) : "Login"}
                    </button>

                    <div className="flex justify-between items-center text-sm text-gray-400">
                        <div className="flex items-center">
                            <input type="checkbox" className="checkbox checkbox-primary mr-2" id="rememberMe" />
                            <label htmlFor="rememberMe">Remember me</label>
                        </div>
                        <a href="#" className="hover:underline">Forgot password?</a>
                    </div>
                    <div className='flex justify-start mt-4'>
                        <a
                            href="#"
                            className="text-sm text-gray-400"
                            onClick={() => navigate('/signup')}
                        >
                            Don't have an account? <span className="text-primary-button hover:underline hover:text-blue-400">Sign up here</span>
                        </a>
                    </div>
                </div>
            </form>
        </div>
    );
};

export default LoginPage;