function x_proj = proj(x, l, u)
    x_proj = min(max(x, l), u);
end