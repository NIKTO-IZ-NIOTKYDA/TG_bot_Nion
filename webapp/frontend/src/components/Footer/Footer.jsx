import React from 'react';
import Button from "../Button/Button";
import {useTelegram} from "../../hooks/useTelegram";
import './Footer.css';

const Footer = () => {
    const {user, onClose} = useTelegram();

    return (
        <div className={'footer'}>
            <Button>Дневник</Button>
            <Button>Расписание</Button>
            <Button>Средний бал</Button>
            <Button>О школе</Button>
        </div>
    );
};

export default Footer;