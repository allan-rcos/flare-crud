import React, {useEffect, useState} from 'react';
import ENV from "../ENV";


function Hello() {
    const [name, setName] = useState('');
    useEffect(() => {
        const fetchData = async () => {
            const result = await fetch(ENV.API_URL() + 'hello/');
            const body = await result.json();
            setName(body['hello']);
        }
        fetchData();
    }, []);
    
    return (
        <h2 className={name===''?'hidden':'text-3xl'}>Hello {name}!</h2>
    );
}

export default Hello;