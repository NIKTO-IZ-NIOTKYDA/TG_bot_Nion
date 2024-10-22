import React from 'react';

const Button = () => {
    const tg = window.Telegram.WebApp

    const onClose = () => {
        tg.close()
    }

    return (
        <div className={'header'}>
            <Button>Закрыть</Button>
            <span className={'username'}>
                {tg.initDataUnsafe?.user?.username}
            </span>
        </div>
    );
};

export default Button