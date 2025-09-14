import React from 'react';
import { UserCircleIcon, LockClosedIcon } from '@heroicons/react/24/outline'; // For icons
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
const SignupPage = () => {

    const [form,setForm] = useState({username:"",email:"",password:""});
    const [loading,setLoading] = useState(false);
    const navigate = useNavigate();

    const handleChange = (e)=>{
        setForm({ ...form, [e.target.name]: e.target.value });
    }

    const handleSignup = async(e)=>{
        e.preventDefault();
        setLoading(true);

        try{
            const res = await fetch('http://localhost:8000/api/auth/signup', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(form),
                credentials: "include"
            })

            const data = await res.json()
            if(!data.error){
                toast.success(data.message)
                window.location.href = `http://localhost:8501/?user_id=${form.email}`;
            }else{
                toast.error(data.error)
            }
        }catch{
            toast.error("Signup Failed")
        }finally{
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
            <form onSubmit={handleSignup}>
                <div className="relative z-10 p-10 py-5 rounded-xl shadow-2xl w-full max-w-md mx-4"
                    style={{ backgroundColor: 'rgba(28, 26, 47, 0.9)', backdropFilter: 'blur(10px)' }}>

                    <div className="flex justify-center mb-4">
                        <UserCircleIcon className="h-24 w-24 text-blue-400" />
                    </div>

                    <div className="form-control mb-4">

                        <label className="input-group input-group-md ">
                            <span className='text-gray-400'>
                                <UserCircleIcon className="h-7 w-7 text-gray-400 mb-1.5" />

                            </span>
                            <input
                                type="text"
                                placeholder="username"
                                id='username'
                                name='username'
                                value={form.username}
                                onChange={handleChange}
                                className="input input-bordered input-md w-full bg-gray-700 text-gray-400 border-gray-600 focus:border-blue-500 focus:ring-blue-500"
                            />
                        </label>
                    </div>
                    <div className="form-control mb-4">

                        <label className="input-group input-group-md">
                            <span>

                                
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-7 mb-1.5 text-gray-400">
                                    <path strokeLinecap="round" strokeLinejoin="round" d="M16.5 12a4.5 4.5 0 1 1-9 0 4.5 4.5 0 0 1 9 0Zm0 0c0 1.657 1.007 3 2.25 3S21 13.657 21 12a9 9 0 1 0-2.636 6.364M16.5 12V8.25" />
                                </svg>
                            </span>
                            <input
                                type="text"
                                placeholder="email"
                                id='email'
                                name='email'
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

                    <button className="btn w-full text-white font-bold py-3 px-4 rounded-lg mb-4"
                        style={{ backgroundColor: '#ff007f', '&:hover': { backgroundColor: '#e60073' } }}>
                        SIGN UP
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
                            onClick={() => navigate('/login')}
                        >
                            Already have an account? <span className="text-primary-button hover:underline hover:text-blue-400">Login </span>
                        </a>
                    </div>
                </div>
            </form>
        </div>
    );
};

export default SignupPage;