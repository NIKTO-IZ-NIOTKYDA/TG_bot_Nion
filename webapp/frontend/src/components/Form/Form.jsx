import React, { useCallback, useEffect, useState } from 'react';
import './Form.css';
import { useTelegram } from "../../hooks/useTelegram";
import { useLocation } from 'react-router-dom';

const Form = () => {
    const [city, setCity] = useState('');
    const [sdekaddress, setSdek] = useState('');
    const [phone, setPhone] = useState('');
    const [subject, setSubject] = useState('physical');
    const [phoneError, setPhoneError] = useState(false);
    const { tg } = useTelegram();
    const location = useLocation();
    const { addedItems } = location.state || { addedItems: [] };

    const onSendData = useCallback(() => {
        const data = {
            city,
            sdekaddress,
            phone,
            addedItems: addedItems.map(item => ({
                id: item.id,
                title: item.title,
                description: item.description,
                selectedSize: item.selectedSize,
                price: item.price,
            })),
        };
        tg.sendData(JSON.stringify(data));
    }, [city, sdekaddress, phone, addedItems]);

    useEffect(() => {
        tg.onEvent('mainButtonClicked', onSendData);
        return () => {
            tg.offEvent('mainButtonClicked', onSendData);
        };
    }, [onSendData]);

    useEffect(() => {
        tg.MainButton.setParams({
            text: 'Отправить данные'
        });
    }, [tg.MainButton]);

    useEffect(() => {
        if (!city || !sdekaddress || !phone || phoneError) {
            tg.MainButton.hide();
        } else {
            tg.MainButton.show();
        }
    }, [city, sdekaddress, phone, phoneError]);

    const onChangeCity = (e) => {
        const value = e.target.value;
        if (/^[a-zA-Zа-яА-Я\s]*$/.test(value)) {
            setCity(value);
        }
    };

    const onChangeSdek = (e) => {
        setSdek(e.target.value);
    };

    const onChangePhone = (e) => {
        const value = e.target.value;
        setPhone(value);
        setPhoneError(!(value.startsWith('+7') && value.length === 12));
    };



    // Функция прокрутки страницы вниз
    const scrollToBottom = () => {
        window.scrollTo({ top: document.documentElement.scrollHeight, behavior: 'smooth' });
    };

    useEffect(() => {
        // Добавляем обработчики событий
        const inputs = document.querySelectorAll('input');
        inputs.forEach(input => {
            input.addEventListener('focus', scrollToBottom);
        });

        window.addEventListener('resize', scrollToBottom);

        // Убираем обработчики событий при размонтировании компонента
        return () => {
            inputs.forEach(input => {
                input.removeEventListener('focus', scrollToBottom);
            });
            window.removeEventListener('resize', scrollToBottom);
        };
    }, []);

    return (
        <div className="form">
            <h3>Товары в корзине</h3>
            <ul className="cart-list">
                {addedItems.length > 0 ? (
                    addedItems.map((item) => (
                        <li key={item.id} className="cart-item">
                            <img src={item.img} alt={item.title} className="cart-item-img" />
                            <div className="cart-item-details">
                                <p className="cart-item-title">{item.title}</p>
                                <p className="cart-item-description">{item.description}</p>
                                <p className="cart-item-size">Размер: {item.selectedSize}</p>
                                <p className="cart-item-price">Цена: {item.price} ₽</p>
                            </div>
                        </li>
                    ))
                ) : (
                    <div>Корзина пуста</div>
                )}
            </ul>

            <h3>Введите ваши данные</h3>
            <input
                className="input"
                type="text"
                placeholder="Город"
                value={city}
                onChange={onChangeCity}
            />
            <input
                className="input"
                type="text"
                placeholder="Адрес"
                value={sdekaddress}
                onChange={onChangeSdek}
            />
            <input
                className="input"
                type="text"
                placeholder="Телефон"
                value={phone}
                onChange={onChangePhone}
            />
            {phoneError && <div className="error">Неправильный номер.</div>}
        </div>
    );
};

export default Form;