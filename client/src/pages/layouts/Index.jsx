import React from 'react';
import SimpleTopNavbar from './patials/SimpleTopNavbar/Navbar';

function Index({children}) {
    return (
        <main>
            <SimpleTopNavbar/>
            {children}
        </main>
    );
}

export default Index;