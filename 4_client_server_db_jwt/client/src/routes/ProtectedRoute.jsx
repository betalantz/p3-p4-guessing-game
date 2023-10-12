import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../providers/authProvider';
import NavMenu from '../components/NavMenu';

export const ProtectedRoute = () => {
    const { token } = useAuth();

    if (!token) {
        return <Navigate to="/login" />;
    }

    return (
        <>
            <NavMenu />
            <Outlet />
        </>
    );
}