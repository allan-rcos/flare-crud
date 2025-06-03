import {BrowserRouter as Router, Navigate, Route, Routes} from "react-router-dom";
import PATHS from "./config/PATHS";
import Login from "./pages/auth/Login";
import Authenticated from "./pages/auth/Authenticated";
import DefaultLayout from './pages/layouts/Index'
import Users from "./pages/models/users/Users";
import NotFound from "./pages/errors/NotFound";


function App() {
    return (
        <Router>
            <Routes>
                <Route path="*" element={<NotFound/>}/>
                <Route path={PATHS.LOGIN} element={<Login/>}/>
                <Route element={<Authenticated/>}>
                    <Route element={<DefaultLayout/>}>
                        <Route path={PATHS.USERS} element={<Users/>}/>
                    </Route>
                </Route>
            </Routes>
        </Router>
    );
}

export default App;
