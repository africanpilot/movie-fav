"use client";

import { PersonInfo } from "@/graphql/schema";


type Props = {
  casts: PersonInfo[];
};

function CastSlide({ casts }: Props) {
  return (
    <div style={{
      display: "grid",
      gridTemplateColumns: "repeat(auto-fill, minmax(90px, 1fr))",
      gap: "10px"
    }}>
        {
            casts.map((item, index) => (
                <div key={index}>
                    <div style={{
                      paddingTop: "160px",
                      backgroundSize: "cover",
                      marginBottom: "0.5rem",
                      backgroundImage: `url(${item?.head_shot})`
                    }}></div>
                    <p style={{fontSize: "0.8rem"}} >{item?.name}</p>
                </div>
            ))
        }
    </div>
  );
}

export default CastSlide;
