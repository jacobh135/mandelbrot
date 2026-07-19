module colormap (
    input wire [4:0] count,
    output reg [1:0] red, green, blue
);
    always @(*) begin
        case (count)
            0: begin
                red = 2'd0;
                green = 2'd0;
                blue = 2'd0;
            end
            1: begin
                red = 2'd0;
                green = 2'd0;
                blue = 2'd1;
            end
            2: begin
                red = 2'd0;
                green = 2'd0;
                blue = 2'd2;
            end
            3: begin
                red = 2'd1;
                green = 2'd0;
                blue = 2'd3;
            end
            4: begin
                red = 2'd0;
                green = 2'd0;
                blue = 2'd3;
            end
            5: begin
                red = 2'd0;
                green = 2'd1;
                blue = 2'd3;
            end
            6: begin
                red = 2'd0;
                green = 2'd1;
                blue = 2'd2;
            end
            7: begin
                red = 2'd0;
                green = 2'd2;
                blue = 2'd3;
            end
            8: begin
                red = 2'd0;
                green = 2'd2;
                blue = 2'd2;
            end
            9: begin
                red = 2'd0;
                green = 2'd3;
                blue = 2'd3;
            end
            10: begin
                red = 2'd1;
                green = 2'd3;
                blue = 2'd3;
            end
            11: begin
                red = 2'd1;
                green = 2'd3;
                blue = 2'd2;
            end
            12: begin
                red = 2'd1;
                green = 2'd3;
                blue = 2'd1;
            end
            13: begin
                red = 2'd2;
                green = 2'd3;
                blue = 2'd1;
            end
            14: begin
                red = 2'd2;
                green = 2'd3;
                blue = 2'd0;
            end
            15: begin
                red = 2'd3;
                green = 2'd3;
                blue = 2'd0;
            end
            16: begin
                red = 2'd3;
                green = 2'd2;
                blue = 2'd0;
            end
            17: begin
                red = 2'd2;
                green = 2'd2;
                blue = 2'd0;
            end
            18: begin
                red = 2'd3;
                green = 2'd1;
                blue = 2'd0;
            end
            19: begin
                red = 2'd2;
                green = 2'd1;
                blue = 2'd0;
            end
            20: begin
                red = 2'd3;
                green = 2'd0;
                blue = 2'd0;
            end
            21: begin
                red = 2'd3;
                green = 2'd0;
                blue = 2'd1;
            end
            22: begin
                red = 2'd2;
                green = 2'd0;
                blue = 2'd0;
            end
            23: begin
                red = 2'd1;
                green = 2'd0;
                blue = 2'd0;
            end
            24: begin
                red = 2'd0;
                green = 2'd0;
                blue = 2'd0;
            end
            default: begin
                red = 2'd0;
                green = 2'd0;
                blue = 2'd0;
            end
        endcase
    end

endmodule