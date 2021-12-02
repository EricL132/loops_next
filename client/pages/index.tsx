import type { NextPage } from "next";
import Head from "next/head";
import Image from "next/image";
import React, { ReactEventHandler, useEffect, useState } from "react";
import styles from "../styles/Home.module.css";
import Link from "next/link";
import { useRouter } from "next/router";
import RightCartInfo from "../Components/RightCartInfo";
interface Showings {
  item: number;
}
interface Products {
  list: Array;
}
const Home: NextPage = () => {
  const [products, setProducts] = useState<Array<{}>>();
  const [currentShowing, setCurrentShowing] = useState<number>();
  const router = useRouter();

  const goToItem = () => {
    router.push(`/pages/product/${products[currentShowing].pid}`);
  };

  const changeCurrent = (e:Event & {target:HTMLButtonElement}) => {
    const {target} = e
    setCurrentShowing(parseInt(target.getAttribute("item")!,10));
    document
      .getElementsByClassName("selected_different_feature_button")[0]
      .classList.remove("selected_different_feature_button");
    target.classList.add("selected_different_feature_button");
  };

  useEffect(() => {
    const getFeature = () => {
      fetch("http://localhost:8000/api/feature")
        .then((res) => res.json())
        .then((data) => {
          console.log(data);
          setCurrentShowing(0);
          setProducts(data);
        });
    };
    getFeature();
  }, []);
  return (
    <div id="home-container">
      {products && currentShowing !== undefined ? (
        <img
          id="featured-item"
          alt=""
          draggable="false"
          src={products[currentShowing].image}
          onClick={goToItem}
        ></img>
      ) : null}

      <div className="home-mid-container">
        <span className="coupon-span">Use code JGFNB3 for 20% off</span>
        <div>
          <Link href="/men/sneakers">
            <button className="home-button mens-button">Mens</button>
          </Link>
          <Link href="women/sneakers">
            <button className="home-button womens-button">Womens</button>
          </Link>
          <Link href="kids/sneakers">
            <button className="home-button kids-button">Kids</button>
          </Link>
        </div>
      </div>
      {products ? (
        <div id="bottom-container-images">
          {products.map((product, i) => {
            if (i === 0) {
              return (
                <button
                  key={i}
                  item={i}
                  className="different_feature_button selected_different_feature_button"
                  onClick={changeCurrent}
                ></button>
              );
            }
            return (
              <button
                key={i}
                item={i}
                className="different_feature_button"
                onClick={changeCurrent}
              ></button>
            );
          })}
        </div>
      ) : null}

      <RightCartInfo></RightCartInfo>
    </div>
  );
};

export default Home;
