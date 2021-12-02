import { useState } from "react"


export default function RightCartInfo() {
    const [showInfo,setShowInfo] = useState()
    return (
        <>
            {showInfo ?
                <div id="cartInfo-overlay" onMouseDown={closeOverlay}>
                    <div id="left-container">
                        <div className="top-row">
                            <h1>Shopping Cart</h1>
                            <button id="cartInfo-close" className="nav-buttons">Close</button>
                        </div>
                        <span className="error-span">{errorMessage}</span>
                        <div id="cartInfo-products-container">
                            {cartInfo ?
                                Object.entries(cartInfo).map((item, i) => {
                                    if (item[1].quantity) {
                                        return <div key={i} className="cartInfo-product-container">
                                            <div className="middle-row">
                                                <img className="cart_image" alt="" src={item[1].image}></img>
                                                <div className="cartInfo-info-container">
                                                    <span className="product-name">{item[1].name}</span>
                                                    <span style={{ display: "block" }}>{item[1].size}</span>
                                                    <div item={item[1].id} className="product-row">
                                                        <button onClick={DecrementItem}>-</button>
                                                        <input className="product-quantity" type="number" defaultValue={item[1].quantity} onKeyDown={changeQuantity} onBlur={changeQuantity}></input>
                                                        <button onClick={IncrementItem}>+</button>
                                                        <button onClick={removeItem}>Remove Item</button>
                                                        <span className="cart_span">${(item[1].quantity * item[1].price).toFixed(2)}</span>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    } else {
                                        return <div key={i} className="cartInfo-product-container">
                                            <div className="middle-row">
                                                <img className="cart_image" alt="" src={item[1].image}></img>
                                                <div className="cartInfo-info-container">
                                                    <span className="product-name">{item[1].name}</span>
                                                    <span style={{ display: "block" }}>{item[1].size}</span>
                                                    <div item={item[1].id} className="product-row">
                                                        <span className="out_of_stock_message">Item is out of stock and was removed from your cart</span>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    }


                                })

                                : null}
                        </div>
                        {bagNum ?
                            <div id="cartInfo-bottom-box">
                                <div id="subtotal">
                                    <span>Subtotal</span>
                                    <span id="subtotal-amount">${subTotal.toFixed(2)}</span>
                                </div>
                                <span id="shipping-text">{"Shipping & taxes calculated at checkout"}</span>
                                <Link to="/pages/checkout"><button id="checkout-button">Checkout</button></Link>
                            </div>
                            : null}


                    </div>

                </div>
                : null}
        </>
    )
}