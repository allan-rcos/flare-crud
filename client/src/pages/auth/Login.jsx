import React, {useState} from 'react';
import { ReactComponent as Logo} from '../../logo.svg'
import ENV from "../../config/ENV";
import {useNavigate} from "react-router-dom";
import PATHS from "../../config/PATHS";

function Login() {
    localStorage.clear();
    const navigate = useNavigate();
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    // TODO: Create a toast message system
    const show_alert = (message) => {
        alert(message);
    }

    const login = async (e) => {
        e.preventDefault();

        let un = username;
        let pw = password

        if (!un?.trim().length)
            un = 'admin';
        if (!pw?.trim().length)
            pw = 'admin';

        const result = await fetch(ENV.API_URL('auth'), {
            method: 'GET',
            headers: {
                'Authorization': 'Basic ' + btoa(un + ":" + pw)
            }
        })
        switch (result.status) {
            case 0:
                console.log(result);
                show_alert('Some issue is causing a zero code')
                break;
            case 200:
                setUsername('');
                setPassword('');
                localStorage.setItem('token', (await result.json())['token']);
                navigate(PATHS.USERS);
                break;
            case 400:
                return show_alert('Server error!?'); // This status code means skip validation.
            case 401:
                return show_alert('Wrong password.');
            case 404:
                return show_alert('User not found.');
            default:
                const json_data = await result.json();
                console.error(json_data);
                return show_alert(json_data['message']);
        }
    }
    return (
        <div className="min-h-screen bg-gray-100 flex flex-col justify-center sm:py-12">
            <div className="p-10 xs:p-0 mx-auto md:w-full md:max-w-md">
                <h1 className="font-bold text-center text-2xl mb-5"><Logo className="mx-auto size-20"/></h1>
                <div className="bg-white shadow w-full rounded-lg divide-y divide-gray-200">
                    <div className="px-5 py-7">
                        <label className="font-semibold text-sm text-gray-600 pb-1 block">Username</label>
                        <input type="text" placeholder="admin" value={username} required
                               onChange={(e) => setUsername(e.target.value)}
                               className="border rounded-lg px-3 py-2 mt-1 mb-5 text-sm w-full"/>
                        <label className="font-semibold text-sm text-gray-600 pb-1 block">Password</label>
                        <input type="password" placeholder="admin" value={password} required
                               onChange={(e) => setPassword(e.target.value)}
                               className="border rounded-lg px-3 py-2 mt-1 mb-5 text-sm w-full"/>
                        <button type="button" onClick={(e) => login(e)}
                                className="transition duration-200 bg-blue-500 hover:bg-blue-600 focus:bg-blue-700 focus:shadow-sm focus:ring-4 focus:ring-blue-500 focus:ring-opacity-50 text-white w-full py-2.5 rounded-lg text-sm shadow-sm hover:shadow-md font-semibold text-center inline-block">
                            <span className="inline-block mr-2">Login</span>
                            <span>&rarr;</span>
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Login;